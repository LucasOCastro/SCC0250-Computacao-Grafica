from OpenGL.GL import *
import numpy as np
from rendering.mesh import Mesh
from rendering.materials import Material

class DrawCall:
    """
    Carrega as informações necessárias para o render em um programa de shader.
    """
    def __init__(self, mesh: Mesh, materials: list[Material], world_transformation_matrix: np.ndarray):
        self.materials = materials
        self.mesh = mesh
        self.world_transformation_matrix = world_transformation_matrix
        