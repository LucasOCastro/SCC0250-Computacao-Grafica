from OpenGL.GL import *
import numpy as np
from typing import List

class Object:
    def __init__(self):
        #TODO consider storing position,scale,rotation separately
        self.local_transformation_matrix = np.identity(4, dtype=np.float32)
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.indices: np.ndarray = []
        self.children: List[Object] = []

    def render(self, parent_transformation_matrix: np.ndarray, set_params: callable) -> None:
        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        for child in self.children:
            child.render(world_mat, set_params)

