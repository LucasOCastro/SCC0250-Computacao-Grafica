from objects.object import Object
import numpy as np
from OpenGL.GL import *
from renderer import Renderer
from matrixmath import *


class MeshObject(Object):
    def __init__(self, render_mode=GL_TRIANGLES):
        super().__init__()

        self.render_mode = render_mode
        self.vertices = np.array([])
        self.indices = np.array([])

        # Criação dos buffers VAO, VBO e EBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

    def _setup_mesh(self):
        """Método privado que une os vértices, normais e cores em um array unificado, e configura o VAO, VBO e EBO."""
        
        # Garante que já temos vértices, normais e indices
        assert self.vertex_positions.size > 0 and self.normals.size > 0 and self.indices.size > 0, "MeshObject's mesh is not initialized. Use set_mesh() method."

        # Junta posições, normais e cores em um único array de vértices
        self.vertices = np.hstack((self.vertex_positions, self.normals, self.colors)).flatten().astype(np.float32)
        
        # Define o contexto como sendo o VAO desse objeto
        glBindVertexArray(self.vao)

        # Envia dados de vértices para GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Envia índices para GPU
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Define o layout dos atributos de vértice no shader
        stride = 10 * self.vertices.itemsize  # 3 (posição) + 3 (normal) + 4 (cor)

        glEnableVertexAttribArray(0)  # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * self.vertices.itemsize))

        glEnableVertexAttribArray(2)  # Cor
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * self.vertices.itemsize))

        # Limpa o contexto do VAO
        glBindVertexArray(0)


    def set_single_color(self, color: tuple):
        '''Define uma única cor para todos os vértices.'''
        colors = np.array([color] * len(self.vertex_positions), dtype=np.float32)
        self.set_colors(colors)

    def set_colors(self, colors: np.ndarray):
        '''Define as cores dos vértices.'''
        self.colors = colors
        self._setup_mesh()

    def set_mesh(self, vertex_positions: np.ndarray, normals: np.ndarray, indices: np.ndarray):
        '''
        Define os dados da mesh, incluindo posições de vértices, normais e índices.
        Reseta a cor para branco.
        '''
        assert vertex_positions.shape[0] == normals.shape[0], "MeshObject's mesh must have the same number of vertices and normals."
        assert vertex_positions.shape[0] > 0 and normals.shape[0] > 0 and indices.shape[0] > 0, "MeshObject's mesh can't be empty."

        self.vertex_positions = vertex_positions
        self.normals = normals
        self.indices = indices
        
        # Reseta a cor e atualiza os dados da mesh (_setup_mesh)
        self.set_single_color((1, 1, 1, 1))


    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        # Super propaga a renderização para os filhos
        super().render(parent_transformation_matrix, renderer)

        # Atualiza matriz de transformação no shader
        world_mat = np.dot(parent_transformation_matrix, self.local_transformation_matrix)
        renderer.set_mat4('mat_transformation', world_mat)

        # Desenha a mesh
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
        """
        Junta várias malhas em uma só, transformando os vértices, normais e índices.
        Aplica a transformação local de cada objeto para os vértices antes de juntar.
        """
        vertex_positions = []
        normals = []
        colors = []
        indices = []

        vertex_count = 0
        for mesh in meshes:
            # Aplica transformação nos vértices
            transform = mesh.local_transformation_matrix
            transformed_positions = [transform_vector(vp, transform) for vp in mesh.vertex_positions]

            # Aplica transformação nos vetores normais (sem translação)
            normal_transform = np.array(mesh.local_transformation_matrix)
            normal_transform[3] = np.array([0, 0, 0, 1])
            transformed_normals = [transform_vector(n, normal_transform) for n in mesh.normals]
            
            vertex_positions.extend(transformed_positions)
            normals.extend(transformed_normals)
            colors.extend(mesh.colors)

            # Ajusta os índices com base no deslocamento atual
            adjusted_indices = mesh.indices + vertex_count
            indices.extend(adjusted_indices)

            vertex_count += len(mesh.vertex_positions)

        combined = MeshObject()
        combined.set_mesh(np.array(vertex_positions), np.array(normals), np.array(indices))
        combined.set_colors(np.array(colors))

        return combined