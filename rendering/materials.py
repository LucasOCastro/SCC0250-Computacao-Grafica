from OpenGL.GL import *
from PIL import Image
import numpy as np
import os
from editablevalue import EditableValue
from rendering.litmode import LitMode

TEXTURE_SUB_FOLDER = 'textures'

class LightParameters:
    """
    Armazena os parâmetros de iluminação de um material.
    vec3 ka; //  coeficiente de reflexao ambiente
    vec3 kd; //  coeficiente de reflexao difusa
    vec3 ks; //  coeficiente de reflexao especular
    float ns; // expoente de reflexao especular
    """
    def __init__(self, 
                 ka: np.ndarray = np.ones(3, dtype=np.float32),
                 kd: np.ndarray = np.ones(3, dtype=np.float32),
                 ks: np.ndarray = np.ones(3, dtype=np.float32),
                 ns: float = 1.0):
        self.ka = np.array(ka, dtype=np.float32)
        self.kd = np.array(kd, dtype=np.float32)
        self.ks = np.array(ks, dtype=np.float32)
        self.ns = ns

    def read_line(self, name: str, value: str) -> None:
        name = name.lower()
        if name == 'ka': self.ka = np.array(value.split(), dtype=np.float32)
        elif name == 'kd': self.kd = np.array(value.split(), dtype=np.float32)
        elif name == 'ks': self.ks = np.array(value.split(), dtype=np.float32)
        elif name == 'ns': self.ns = float(value)

class Material:
    """
    Representa uma instância de material simples.

    Em uma engine real, dados de material (textura) e de aplicação a mesh (ebo, indices) seriam separados. 
    Por simplicidade, unimos os conceitos, dado que nosso projeto não usa o mesmo material em modelos diferentes.
    """
    def __init__(self, texture_path: str, 
                 light_parameters: LightParameters = LightParameters(),
                 color_multiplier_editable: EditableValue = None,
                 lit_mode: LitMode = LitMode.LIT,
                 wrap_type = GL_REPEAT,
                 filter_type = GL_LINEAR):
        self.texture_id = None
        self.ebo = None
        self.indices = None
        
        self.light_parameters = light_parameters
        self.color_multiplier_editable = color_multiplier_editable
        self.lit_mode = lit_mode
        if color_multiplier_editable is None:
            self.color_multiplier_editable = EditableValue(1.0, 0.35, 1.5, 'Cor')

        self._load_texture(texture_path, wrap_type, filter_type)

    @property
    def color_multiplier(self) -> float:
        return self.color_multiplier_editable.value

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
    def try_load_material(file_name: str, root_path: str, light_parameters: LightParameters = LightParameters()):
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
        current_light_parameters: LightParameters = None
        
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
                    current_light_parameters = LightParameters()
                elif values[0] == 'map_Kd': # albedo
                    file_name = os.path.basename(values[1])
                    new_material = Material.try_load_material(file_name, folder, light_parameters=current_light_parameters)
                    self.materials[current_material_name] = new_material
                    # reseta
                    current_material_name = None
                    current_light_parameters = None
                elif current_light_parameters is not None: # parametros de luz (ks, kd, etc)
                    current_light_parameters.read_line(values[0], values[1])

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