import numpy as np
from OpenGL.GL import *
from PIL import Image
import os

TEXTURE_SUB_FOLDER = 'textures'

class Material:
    """
    Usually, a material would only keep global info, such as texture. 
    Then a MaterialInstance would have an ebo, indices, and general unique info.
    For simplicity, we merged both concepts.
    """
    def __init__(self, texture_path: str):
        self.texture_id = None
        self.ebo = None
        self.indices = None
        self._load_texture(texture_path)

    def _load_texture(self, texture_path: str) -> None:
        self.texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img = Image.open(texture_path).convert("RGBA")
        img_width, img_height = img.size
        image_data = img.tobytes("raw", "RGBA", 0, -1)
        # Allocate an RGBA texture on the GPU:
        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA,
            img_width, img_height, 0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data
        )

    def setup_ebo(self, indices: np.ndarray) -> None:
        "Remember to bind the vao before calling this."
        indices = np.array(indices, dtype=np.uint32)
        self.ebo = glGenBuffers(1)
        self.indices = indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    def render(self):
        "Remember to bind the vao before calling this."
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def destroy(self):
        glDeleteTextures([self.texture_id])

class MaterialLibrary:
    def __init__(self):
        self.materials = {}

    def load_mtl(self, mtl_path: str) -> None:
        if not os.path.exists(mtl_path):
            print(f"Material file {mtl_path} does not exist")
            return

        folder = os.path.dirname(mtl_path)
        current_material_name = None
        
        with open(mtl_path, "r") as file:
            for line in file:
                values = line.strip().split(maxsplit=1)
                if not values:
                    continue

                if values[0] == 'newmtl':
                    if current_material_name is not None:
                        print(f"Material {current_material_name} has no texture")
                        self.materials[current_material_name] = None
                    current_material_name = values[1]
                elif values[0] == 'map_Kd':
                    file_name = os.path.basename(values[1])
                    file_path = os.path.join(folder, TEXTURE_SUB_FOLDER, file_name)
                    self.materials[current_material_name] = Material(file_path)
                    current_material_name = None

        if current_material_name is not None:
            print(f"Material {current_material_name} has no texture")
            self.materials[current_material_name] = None

    def get(self, material_name: str) -> Material:
        return self.materials[material_name]

    def get_or_default(self, material_name: str) -> Material:
        if material_name in self.materials:
            return self.materials[material_name]
        
        if None in self.materials:
            print(f"Material {material_name} does not exist, using default material")
            return self.materials[None]
        
        print("Materials:")
        for material_name, material in self.materials.items():
            print(f"- {material_name}: {material}")
        
        
        raise Exception(f"Material {material_name} does not exist and there is no default material")
    
    def set(self, material_name: str, material: Material):
        self.materials[material_name] = material
    
    def destroy(self):
        for material in self.materials.values():
            if material is not None:
                material.destroy()