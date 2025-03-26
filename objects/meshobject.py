from objects.object import Object
import numpy as np
from OpenGL.GL import *


class MeshObject(Object):
    def __init__(self, color: tuple, vertices: np.ndarray, indices: np.ndarray):
        super().__init__()
        self.color = color
        self.vertices = vertices
        self.indices = indices
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self._setup_mesh()

    def _setup_mesh(self):
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)  # Position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * self.vertices.itemsize, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * self.vertices.itemsize, ctypes.c_void_p(3 * self.vertices.itemsize))

        glBindVertexArray(0)

    def render(self, parent_transformation_matrix: np.ndarray, set_params: callable) -> None:
        super().render(parent_transformation_matrix, set_params)

        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        set_params(self.color, world_mat)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)