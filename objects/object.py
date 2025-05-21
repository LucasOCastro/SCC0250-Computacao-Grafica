from OpenGL.GL import *
import numpy as np
from typing import List
from matrixmath import *

class Object:
    def __init__(self):
        self.model_matrix = np.identity(4, dtype=np.float32)
        self.world_transformation_matrix = np.identity(4, dtype=np.float32)
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.parent: 'Object' = None

        self.indices: np.ndarray = []
        self.children: List[Object] = []

    def refresh_model_matrix(self):
        """Recalcula a matriz local com base nas transformações atuais"""
        translation_mat = translation_matrix(self.position)
        rotation_mat = rotation_matrix_all(self.rotation)
        scale_mat = scale_matrix(self.scale)

        new_matrix = multiply_transformations([
            translation_mat,
            rotation_mat,
            scale_mat,
        ])

        if np.any(new_matrix != self.model_matrix):
            self.model_matrix = new_matrix
            self.refresh_world_matrix()
    
    def refresh_world_matrix(self):
        """Recalcula a matriz global com base na global do pai e a model local."""
        new_matrix = np.identity(4, dtype=np.float32)
        if self.parent:
            new_matrix = multiply_transformations([
                self.parent.world_transformation_matrix,
                self.model_matrix
            ])
        else:
            new_matrix = self.model_matrix
        
        if np.any(new_matrix != self.world_transformation_matrix):
            self.world_transformation_matrix = new_matrix
            for child in self.children:
                child.refresh_world_matrix()
    
    def add_child(self, child: 'Object'):
        self.children.append(child)
        child.set_parent(self)
    
    def add_children(self, children: List['Object']):
        for child in children:
            self.add_child(child)
    
    def remove_child(self, child: 'Object'):
        self.children.remove(child)
        child.set_parent(None)

    def set_parent(self, parent: 'Object'):
        self.parent = parent
        self.refresh_world_matrix()

    def set_pos(self, pos: np.ndarray):
        self.position = np.array(pos, dtype=np.float32)
        self.refresh_model_matrix()

    def translate(self, delta: np.ndarray):
        self.position += delta
        # TODO propert gradual change
        self.set_pos(self.position)
        

    def set_rot_rad(self, rot: np.ndarray):
        self.rotation = np.array(rot, dtype=np.float32)
        self.refresh_model_matrix()

    def set_rot_deg(self, rot: np.ndarray):
        self.set_rot_rad(np.deg2rad(rot))

    def rotate_rad(self, radian: float, axis: np.ndarray, around_self: bool = False):
        if around_self:
            temp_position = np.array(self.position) # Clone because it will be modified
            self.translate(-temp_position)

        rotation = np.array(axis) * radian
        self.rotation += rotation
        rotation_mat = rotation_matrix_all(rotation)
        # TODO propert gradual change
        self.set_rot_rad(self.rotation)

        if around_self:
            self.translate(temp_position)

    def rotate_deg(self, degree: float, axis: np.ndarray, around_self: bool = False):
        self.rotate_rad(np.deg2rad(degree), axis, around_self=around_self)

    def set_scale(self, scale: np.ndarray):
        self.scale = np.array(scale, dtype=np.float32)
        self.refresh_model_matrix()
    
    def set_scale_single(self, scale: float):
        self.set_scale(np.array([scale, scale, scale], dtype=np.float32))

    def world_to_local(self, point: np.ndarray) -> np.ndarray:
        """Converte ponto do mundo para o espaço local do objeto"""
        return transform_vector(point, np.linalg.inv(self.world_transformation_matrix))
    
    def local_to_world(self, point: np.ndarray) -> np.ndarray:
        """Converte ponto do espaço local do objeto para o mundo"""
        return transform_vector(point, self.world_transformation_matrix)
    
    @property
    def world_position(self):
        return self.world_transformation_matrix[:3, 3]

    def destroy(self):
        """Destrói o objeto e seus filhos"""
        for child in self.children:
            child.destroy()

    def update(self, *args):
        """Atualiza o objeto e seus filhos"""
        for child in self.children:
            child.update(*args)
    
    # TODO lit/unlit materials
    def collect(self, action: callable):
        for child in self.children:
            child.collect(action)
        action(self)