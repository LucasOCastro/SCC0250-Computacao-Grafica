from objects.meshobject import MeshObject
import numpy as np

class Cube(MeshObject):
    def __init__(self, size=1.0, single_color=(1, 1, 1, 1), face_colors: list=None):
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

        if (face_colors is None):
            face_colors = [single_color] * 6
        colors = np.array([
            # Front
            face_colors[0], face_colors[0], face_colors[0], face_colors[0],
            # Back
            face_colors[1], face_colors[1], face_colors[1], face_colors[1],
            # Left
            face_colors[2], face_colors[2], face_colors[2], face_colors[2],
            # Right
            face_colors[3], face_colors[3], face_colors[3], face_colors[3],
            # Top
            face_colors[4], face_colors[4], face_colors[4], face_colors[4],
            # Bottom
            face_colors[5], face_colors[5], face_colors[5], face_colors[5]
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2, 2, 3, 0,  # Front
            4, 5, 6, 6, 7, 4,  # Back
            8, 9, 10, 10, 11, 8,  # Left
            12, 13, 14, 14, 15, 12,  # Right
            16, 17, 18, 18, 19, 16,  # Top
            20, 21, 22, 22, 23, 20   # Bottom
        ], dtype=np.uint32)

        # Call set_data method from BaseMesh
        self.set_data(vertices, normals, colors, indices)