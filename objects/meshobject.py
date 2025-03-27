from objects.object import Object
import numpy as np
from OpenGL.GL import *
from renderer import Renderer


class MeshObject(Object):
    def __init__(self):
        super().__init__()
        self.vertices = np.array([])
        self.indices = np.array([])
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

    def __del__(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        glDeleteBuffers(1, (self.ebo,))

    def _setup_mesh(self):
        assert self.vertices.size > 0 and self.indices.size > 0, "MeshObject's mesh is not initialized. Use set_data() method."

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        stride = 10 * self.vertices.itemsize  # 3 (position) + 3 (normal) + 4 (color)

        glEnableVertexAttribArray(0)  # Position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * self.vertices.itemsize))

        glEnableVertexAttribArray(2)  # Color
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * self.vertices.itemsize))

        glBindVertexArray(0)

    def set_data(self, vertices: np.ndarray, normals: np.ndarray, colors: np.ndarray, indices: np.ndarray):
        self.vertices = np.hstack((vertices, normals, colors)).flatten().astype(np.float32)
        self.indices = indices
        self._setup_mesh()


    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        super().render(parent_transformation_matrix, renderer)

        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        renderer.set_mat4('mat_transformation', world_mat)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)