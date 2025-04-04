from objects.object import Object
import numpy as np
from OpenGL.GL import *
from renderer import Renderer


class MeshObject(Object):
    def __init__(self, render_mode=GL_TRIANGLES):
        super().__init__()
        self.render_mode = render_mode
        self.vertices = np.array([])
        self.indices = np.array([])
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

    def _setup_mesh(self):
        assert self.vertex_positions.size > 0 and self.normals.size > 0 and self.indices.size > 0, "MeshObject's mesh is not initialized. Use set_mesh() method."

        self.vertices = np.hstack((self.vertex_positions, self.normals, self.colors)).flatten().astype(np.float32)
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


    def set_single_color(self, color: tuple):
        '''Sets a single color for all vertices of the mesh.'''
        colors = np.array([color] * len(self.vertex_positions), dtype=np.float32)
        self.set_colors(colors)

    def set_colors(self, colors: np.ndarray):
        '''Sets the vertex colors.'''
        self.colors = colors
        self._setup_mesh()

    def set_mesh(self, vertex_positions: np.ndarray, normals: np.ndarray, indices: np.ndarray):
        '''
        Sets the mesh data, including vertex positions, normals and indices.
        Resets the color to white.
        '''
        assert vertex_positions.shape[0] == normals.shape[0], "MeshObject's mesh must have the same number of vertices and normals."
        assert vertex_positions.shape[0] > 0 and normals.shape[0] > 0 and indices.shape[0] > 0, "MeshObject's mesh can't be empty."

        self.vertex_positions = vertex_positions
        self.normals = normals
        self.indices = indices
        # Reset color to white and update mesh data
        self.set_single_color((1, 1, 1, 1))


    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        super().render(parent_transformation_matrix, renderer)

        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        renderer.set_mat4('mat_transformation', world_mat)

        glBindVertexArray(self.vao)
        glDrawElements(self.render_mode, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def destroy(self):
        super().destroy()
        
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        glDeleteBuffers(1, [self.ebo])


    @staticmethod
    def merge_meshes(meshes: list["MeshObject"]) -> "MeshObject":
        vertex_positions = []
        normals = []
        colors = []
        indices = []

        vertex_count = 0
        for mesh in meshes:
            # Apply transform to vertex positions
            transform = mesh.local_transformation_matrix
            transformed_positions = [transform @ np.array([*vp, 1]) for vp in mesh.vertex_positions]
            transformed_positions = [vp[:3] for vp in transformed_positions]

            # Apply transform to normals (ignore translation)
            normal_transform = np.array(mesh.local_transformation_matrix)
            normal_transform[3] = np.array([0, 0, 0, 1])
            transformed_normals = [normal_transform @ np.array([*n, 1]) for n in mesh.normals]
            transformed_normals = [n[:3] for n in transformed_normals]
            
            vertex_positions.extend(transformed_positions)
            normals.extend(transformed_normals)
            colors.extend(mesh.colors)

            adjusted_indices = mesh.indices + vertex_count
            indices.extend(adjusted_indices)

            vertex_count += len(mesh.vertex_positions)

        combined = MeshObject()
        combined.set_mesh(np.array(vertex_positions), np.array(normals), np.array(indices))
        combined.set_colors(np.array(colors))

        return combined