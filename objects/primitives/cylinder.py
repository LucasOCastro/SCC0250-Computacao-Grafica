from objects.meshobject import MeshObject
import numpy as np

from OpenGL.GL import *

class Cylinder(MeshObject):

    def __init__(self, slices=36, radius=0.5, length=0.5, top_color=(1, 1, 1, 1), bottom_color=(1, 1, 1, 1), side_color=(1, 1, 1, 1)):
        super().__init__(render_mode=GL_TRIANGLE_STRIP)
        self.radius = radius
        self.length = length
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.side_color = side_color

        vertices = []
        normals = []
        indices = []

        angle_step = 2 * np.pi / slices

        # Criar vértices e normais para a lateral
        for i in range(slices + 1):
            angle = i * angle_step
            x = np.cos(angle) * radius
            y = np.sin(angle) * radius

            # Topo
            vertices.append([x, y, length / 2])   # Posição
            normals.append([x, y, 0])             # Normal

            # Base
            vertices.append([x, y, -length / 2])
            normals.append([x, y, 0])

        # Criar índice da lateral (GL_TRIANGLE_STRIP)
        for i in range(slices):
            indices.extend([i * 2, i * 2 + 1])

        # Adicionar vértices centrais para as tampas
        top_center_index = len(vertices) // 3
        bottom_center_index = top_center_index + 1

        vertices.append([0, 0, length / 2])   # Centro do topo
        normals.append([0, 0, 1])             # Normal para cima
        vertices.append([0, 0, -length / 2])  # Centro da base
        normals.append([0, 0, -1])            # Normal para baixo

        # Criar os índices para as tampas
        for i in range(slices):
            next_i = (i + 1) % slices

            # Triângulos do topo
            indices.extend([top_center_index, i * 2, next_i * 2])

            # Triângulos da base
            indices.extend([bottom_center_index, next_i * 2 + 1, i * 2 + 1])

        # Converter para numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        normals = np.array(normals, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        self.set_mesh(vertices, normals, indices)
        self.set_single_color(top_color)      