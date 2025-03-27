from OpenGL.GL import *
import numpy as np
from typing import List
from matrixmath import *
from renderer import Renderer

class Object:
    def __init__(self):
        self.local_transformation_matrix = np.identity(4, dtype=np.float32)
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.indices: np.ndarray = []
        self.children: List[Object] = []
        self.pivot = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    #TODO consider incremental matrix modification for translate, rotate, scale, etc
    def refresh_transformation_matrix(self):
        translation_mat = translation_matrix(self.position)
        pivot_translation = translation_matrix(-self.pivot)
        pivot_back_translation = translation_matrix(self.pivot)

        rot_x = rotation_matrix_x(self.rotation[0])
        rot_y = rotation_matrix_y(self.rotation[1])
        rot_z = rotation_matrix_z(self.rotation[2])
        rotation_mat = np.dot(rot_z, np.dot(rot_y, rot_x))

        scale_mat = scale_matrix(self.scale)

        self.local_transformation_matrix = translation_mat @ pivot_back_translation @ rotation_mat @ scale_mat @ pivot_translation


    def set_pos(self, pos: np.ndarray):
        self.position = np.array(pos, dtype=np.float32)
        self.refresh_transformation_matrix()

    def set_rot_rad(self, rot: np.ndarray):
        self.rotation = np.array(rot, dtype=np.float32)
        self.refresh_transformation_matrix()

    def set_rot_deg(self, rot: np.ndarray):
        self.set_rot_rad(np.deg2rad(rot))

    def set_scale(self, scale: np.ndarray):
        self.scale = np.array(scale, dtype=np.float32)
        self.refresh_transformation_matrix()

    def set_pivot(self, pivot: np.ndarray):
        self.pivot = np.array(pivot, dtype=np.float32)
        self.refresh_transformation_matrix()

    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        for child in self.children:
            child.render(world_mat, renderer)

