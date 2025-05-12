import os
import numpy as np
from OpenGL.GL import *
from renderer import Renderer
from objects.object import Object
from mesh import Mesh

class MeshObject(Object):
    def __init__(self, obj_sub_dir: str, default_texture_path: str | None = None):
        super().__init__()
        
        self.mesh = Mesh.from_path(obj_sub_dir, default_texture_path)

    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        # Super propaga a renderização para os filhos
        super().render(parent_transformation_matrix, renderer)

        # Atualiza matriz de transformação no shader e renderiza
        world_mat = np.dot(parent_transformation_matrix, self.model_matrix)
        renderer.set_mat4('model', world_mat)
        self.mesh.render()