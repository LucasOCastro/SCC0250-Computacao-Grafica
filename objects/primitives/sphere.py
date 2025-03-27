from objects.meshobject import MeshObject
import numpy as np

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