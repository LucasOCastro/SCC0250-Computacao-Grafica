from objects.meshobject import MeshObject
import numpy as np

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

        # color = np.array([color], dtype=np.float32)
        new_colors = self.colors.copy()
        new_colors[start:end] = color
        self.set_colors(new_colors)
