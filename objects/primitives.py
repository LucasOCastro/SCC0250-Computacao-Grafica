from objects.meshobject import MeshObject
import numpy as np
from OpenGL.GL import GL_TRIANGLE_STRIP
from matrixmath import *

class Cube(MeshObject):
    FRONT = 0
    BACK = 1
    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5

    def __init__(self, size=1.0, color=(1, 1, 1, 1)):
        super().__init__()

        vertices = np.array([
            # Front face
            [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1],
            # Back face
            [-1, -1, -1], [-1,  1, -1], [ 1,  1, -1], [ 1, -1, -1],
            # Left face
            [-1, -1, -1], [-1, -1,  1], [-1,  1,  1], [-1,  1, -1],
            # Right face
            [ 1, -1, -1], [ 1,  1, -1], [ 1,  1,  1], [ 1, -1,  1],
            # Top face
            [-1,  1, -1], [ 1,  1, -1], [ 1,  1,  1], [-1,  1,  1],
            # Bottom face
            [-1, -1, -1], [-1, -1,  1], [ 1, -1,  1], [ 1, -1, -1]
        ], dtype=np.float32) * size / 2

        normals = np.array([
            # Front
            [ 0,  0,  1], [ 0,  0,  1], [ 0,  0,  1], [ 0,  0,  1],
            # Back
            [ 0,  0, -1], [ 0,  0, -1], [ 0,  0, -1], [ 0,  0, -1],
            # Left
            [-1,  0,  0], [-1,  0,  0], [-1,  0,  0], [-1,  0,  0],
            # Right
            [ 1,  0,  0], [ 1,  0,  0], [ 1,  0,  0], [ 1,  0,  0],
            # Top
            [ 0,  1,  0], [ 0,  1,  0], [ 0,  1,  0], [ 0,  1,  0],
            # Bottom
            [ 0, -1,  0], [ 0, -1,  0], [ 0, -1,  0], [ 0, -1,  0]
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2, 2, 3, 0,  # Front
            4, 5, 6, 6, 7, 4,  # Back
            8, 9, 10, 10, 11, 8,  # Left
            12, 13, 14, 14, 15, 12,  # Right
            16, 17, 18, 18, 19, 16,  # Top
            20, 21, 22, 22, 23, 20   # Bottom
        ], dtype=np.uint32)

        self.set_mesh(vertices, normals, indices)
        self.set_single_color(color)

    def set_face_color(self, face: int, color: tuple):
        start = face * 4
        end = start + 4

        new_colors = self.colors.copy()
        new_colors[start:end] = color
        self.set_colors(new_colors)


class Sphere(MeshObject):
    def __init__(self, radius: float = 0.5, slices: int = 16, stacks: int = 16, color: tuple = (1, 1, 1, 1)):
        super().__init__()
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

        vertices = np.zeros(((stacks + 1) * (slices + 1), 3), dtype=np.float32)
        normals = np.zeros(((stacks + 1) * (slices + 1), 3), dtype=np.float32)
        indices = np.zeros(stacks * slices * 6, dtype=np.uint32)  # Each quad has 2 triangles = 6 indices

        # Generate vertices and normals
        index = 0
        for i in range(stacks + 1):
            for j in range(slices + 1):
                theta = i * np.pi / stacks
                phi = j * 2 * np.pi / slices
                x = radius * np.sin(theta) * np.cos(phi)
                y = radius * np.cos(theta)
                z = radius * np.sin(theta) * np.sin(phi)

                vertices[index] = [x, y, z]
                normals[index] = [x, y, z]
                index += 1

        # Generate indices
        index = 0
        for i in range(stacks):
            for j in range(slices):
                first = i * (slices + 1) + j
                second = first + slices + 1

                # First triangle
                indices[index] = first
                indices[index + 1] = second
                indices[index + 2] = first + 1

                # Second triangle
                indices[index + 3] = second
                indices[index + 4] = second + 1
                indices[index + 5] = first + 1

                index += 6
        
        self.set_mesh(vertices, normals, indices)
        self.set_single_color(color)


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
            z = np.sin(angle) * radius

            # Topo
            vertices.append([x, length / 2, z])   # Posição
            normals.append([x, 0, z])             # Normal

            # Base
            vertices.append([x,-length / 2, z])
            normals.append([x, 0, z])

        # Criar índice da lateral 
        for i in range(slices):
            indices.extend([i * 2, i * 2 + 1])

        # Adicionar vértices centrais para as tampas
        top_center_index = len(vertices) // 3
        bottom_center_index = top_center_index + 1

        vertices.append([0, length / 2, 0])   # Centro do topo
        normals.append([0, 1, 0])             # Normal para cima
        vertices.append([0, -length / 2, 0 ])  # Centro da base
        normals.append([0, -1, 0])            # Normal para baixo

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