import numpy as np
from OpenGL.GL import *
from PIL import Image
import os

TEXTURE_SUB_FOLDER = 'textures'

class Material:
    """
    Representa uma instância de material simples, definido por um arquivo de textura (ignoramos rugosidade, especularidade, etc).

    Em uma engine real, dados de material (textura) e de uso (ebo, indices) seriam separados.
    Por simplicidade, unimos os dois conceitos, dado que nosso projeto não usa o mesmo material em modelos diferentes.
    """
    def __init__(self, texture_path: str, 
                 light_parameters: dict[str, np.ndarray | float] = {},
                 wrap_type = GL_REPEAT,
                 filter_type = GL_LINEAR):
        self.texture_id = None
        self.ebo = None
        self.indices = None
        self.light_parameters = light_parameters
        self._load_texture(texture_path, wrap_type, filter_type)

    def _load_texture(self, texture_path: str, wrap_type, filter_type) -> None:
        self.texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        self.set_wrap_mode(wrap_type)
        self.set_filter_mode(filter_type)

        img = Image.open(texture_path).convert("RGBA")
        img_width, img_height = img.size
        image_data = img.tobytes("raw", "RGBA", 0, -1)
        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA,
            img_width, img_height, 0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data
        )
    
    @property
    def is_lit(self) -> bool:
        return len(self.light_parameters) > 0

    def set_wrap_mode(self, wrap_type):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_type)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_type)

    def set_filter_mode(self, filter_type):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_type)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_type)

    def setup_ebo(self, indices: np.ndarray) -> None:
        """
        Deve ser chamado após um VAO (Vertex Array Object) ter sido vinculado.
        Configura o Element Buffer Object (EBO) com os índices que serão usados para renderizar o modelo.
        """
        indices = np.array(indices, dtype=np.uint32)
        self.ebo = glGenBuffers(1)
        self.indices = indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    def destroy(self):
        glDeleteTextures([self.texture_id])
        if self.ebo is not None:
            glDeleteBuffers(1, [self.ebo])

    @staticmethod
    def try_load_material(file_name: str, root_path: str, light_parameters: dict[str, np.ndarray | float] = {}):
        
        """
        Tenta carregar um material a partir de uma textura. 
        Tenta primeiro em 'root_path/textures/file_name', depois em 'root_path/file_name'.
        Se não conseguir, lança uma exceção.
        """
        file_path = os.path.join(root_path, TEXTURE_SUB_FOLDER, file_name)
        if os.path.isfile(file_path):
            return Material(file_path, light_parameters=light_parameters)
        
        file_path = os.path.join(root_path, file_name)
        if os.path.isfile(file_path):
            return Material(file_path, light_parameters=light_parameters)
        
        raise Exception(f"Could not find texture {file_name} in {root_path}")

class MaterialLibrary:
    """
    Classe que representa uma biblioteca de materiais, indexados por nome.
    É a versão em memória de um arquivo .mtl
    """
    def __init__(self):
        self.materials: dict[str, Material] = {}

    def load_mtl(self, mtl_path: str) -> None:
        if not os.path.exists(mtl_path):
            print(f"Mtl file {mtl_path} does not exist")
            return

        folder = os.path.dirname(mtl_path)
        current_material_name = None
        current_light_parameters: dict[str, np.ndarray | float] = {}
        
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
                    current_light_parameters = {}
                elif values[0] == 'map_Kd': # albedo
                    file_name = os.path.basename(values[1])                    
                    new_material = Material.try_load_material(file_name, folder, light_parameters=current_light_parameters)
                    self.materials[current_material_name] = new_material

                    current_material_name = None
                    current_light_parameters = {}
                else: # parametros de luz (ks, kd, etc)
                    try:
                        params = values[1].split()
                        name = values[0].strip().lower()
                        if len(params) == 1:
                            current_light_parameters[name] = float(params[0])
                        else:
                            current_light_parameters[name] = np.array([float(param) for param in params], dtype=np.float32)
                    except ValueError:
                        pass

        if current_material_name is not None:
            print(f"Material {current_material_name} has no texture")
            self.materials[current_material_name] = None

    def get_or_default(self, material_name: str) -> Material:
        """
        Retorna o material com o nome fornecido, ou o material padrão se ele não existir.
        Se nem o material nem o padrão existirem, lança uma exceção.
        """
        if material_name in self.materials and self.materials[material_name] is not None:
            return self.materials[material_name]
        
        if None in self.materials:
            print(f"Material {material_name} does not exist, using default material")
            return self.materials[None]
        
        raise Exception(f"Material {material_name} does not exist and there is no default material")
    
    def get_default(self) -> Material:
        return self.materials[None]
    
    def set(self, material_name: str, material: Material):
        self.materials[material_name] = material   
    
    def destroy(self):
        for material in self.materials.values():
            if material is not None:
                material.destroy()