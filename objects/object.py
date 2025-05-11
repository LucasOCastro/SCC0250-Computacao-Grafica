from OpenGL.GL import *
import numpy as np
from typing import List
from matrixmath import *
from renderer import Renderer

class Object:
    def __init__(self):
        self.model_matrix = np.identity(4, dtype=np.float32)
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        self.indices: np.ndarray = []
        self.children: List[Object] = []

    def refresh_model_matrix(self):
        """Recalcula a matriz local com base nas transformações atuais"""
        translation_mat = translation_matrix(self.position)
        rotation_mat = rotation_matrix_all(self.rotation)
        scale_mat = scale_matrix(self.scale)

        self.model_matrix = multiply_transformations([
            translation_mat,
            rotation_mat,
            scale_mat,
        ])


    def set_pos(self, pos: np.ndarray):
        self.position = np.array(pos, dtype=np.float32)
        self.refresh_model_matrix()

    def translate(self, delta: np.ndarray):
        self.position += delta
        translation_mat = translation_matrix(delta)
        self.model_matrix = multiply_transformations([translation_mat, self.model_matrix])

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
        self.model_matrix = multiply_transformations([rotation_mat, self.model_matrix])

        if around_self:
            self.translate(temp_position)

    def rotate_deg(self, degree: float, axis: np.ndarray, around_self: bool = False):
        self.rotate_rad(np.deg2rad(degree), axis, around_self=around_self)

    def set_scale(self, scale: np.ndarray):
        self.scale = np.array(scale, dtype=np.float32)
        self.refresh_model_matrix()
    
    def set_scale_single(self, scale: float):
        self.set_scale(np.array([scale, scale, scale], dtype=np.float32))

    def scale_by(self, scale: np.ndarray):
        self.scale += scale
        scale_mat = scale_matrix(scale)
        self.model_matrix = multiply_transformations([scale_mat, self.model_matrix])

    def scale_by_single(self, scale: float):
        self.scale_by(np.array([scale, scale, scale], dtype=np.float32))

    def world_to_local(self, point: np.ndarray) -> np.ndarray:
        """Converte ponto do mundo para o espaço local do objeto"""
        return transform_vector(point, np.linalg.inv(self.model_matrix))
    
    def local_to_world(self, point: np.ndarray) -> np.ndarray:
        """Converte ponto do espaço local do objeto para o mundo"""
        return transform_vector(point, self.model_matrix)

    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        """Renderiza o objeto e seus filhos com base na matriz do pai"""
        world_mat = np.dot(parent_transformation_matrix, self.model_matrix)
        for child in self.children:
            child.render(world_mat, renderer)

    def destroy(self):
        """Destrói o objeto e seus filhos"""
        for child in self.children:
            child.destroy()

    def update(self, *args):
        """Atualiza o objeto e seus filhos"""
        for child in self.children:
            child.update(*args)
