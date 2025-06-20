import numpy as np
from OpenGL.GL import *
from rendering.materials import MaterialLibrary, Material
import os

ASSETS_SUB_FOLDER = 'assets'

loaded_meshes = {}

class Mesh:
    """
    Objeto que representa um mesh carregado de um arquivo .obj
    """
    def __init__(self, obj_path: str, default_texture_path: str | None = None):
        self.obj_name = os.path.basename(obj_path).rstrip(".obj")
        self.asset_sub_folder = os.path.join(ASSETS_SUB_FOLDER, os.path.dirname(obj_path))

        # Criação dos buffers
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        # Carrega a textura padrão, se existir
        self.material_library = MaterialLibrary()
        if default_texture_path is not None:
            default_material = Material.try_load_material(default_texture_path, self.asset_sub_folder)
            self.material_library.set(None, default_material)

        # Carrega o modelo
        self._load_obj(os.path.join(ASSETS_SUB_FOLDER, obj_path))

        # Verifica erro
        error = glGetError()
        if error != GL_NO_ERROR:
            print(error)
            raise Exception("OpenGL error when creating object")

    def destroy(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        self.material_library.destroy()

    def _load_obj(self, obj_path: str):
        raw_vertex_list = []
        raw_uv_list = []
        raw_vn_list = []
        
        vertices = []
        material_indices = {}
        unique_vertex_map = {}

        current_mat = None
        with open(obj_path, "r") as file:
            for line in file:
                values = line.strip().split()
                if not values:
                    continue
                ### recuperando materiais
                if values[0] == 'mtllib':
                    path = " ".join(values[1:])
                    mtl_path = os.path.join(self.asset_sub_folder, path)
                    self.material_library.load_mtl(mtl_path)
                elif values[0] == 'usemtl':
                    current_mat = values[1]
                ### recuperando vertices
                elif values[0] == 'v':
                    raw_vertex_list.append(values[1:4])
                ### recuperando coordenadas de textura
                elif values[0] == 'vt':
                    raw_uv_list.append(values[1:3])
                ### recuperando normais
                elif values[0] == 'vn':
                    raw_vn_list.append(values[1:4])
                ### recuperando faces 
                elif values[0] == 'f':
                    face = self._circular_sliding_window_of_three(values[1:])
                    for v in face:
                        # no .obj uma face é definida por indice_vertice/indice_vt/indice_vn
                        # nesse trabalho não usaremos normais (vn)
                        parts = v.split('/')
                        if len(parts) == 1:
                            print(f"Face sem coordenada de textura em {obj_path}")
                            continue

                        vertex_idx = int(parts[0])
                        uv_idx = int(parts[1])
                        vn_idx = int(parts[2]) if len(parts) > 2 else None

                        # índices negativos são do fim da lista
                        if vertex_idx < 0: 
                            vertex_idx += len(raw_vertex_list) + 1
                        if uv_idx < 0:
                            uv_idx += len(raw_uv_list) + 1
                        if vn_idx is not None and vn_idx < 0:
                            vn_idx += len(raw_vn_list) + 1

                        # prepara para armazenar os indices no material atual
                        if current_mat not in material_indices:
                            material_indices[current_mat] = []
                        indices = material_indices[current_mat]

                        # mantemos unicidade das tuplas vertice/uv/vn
                        key = (vertex_idx, uv_idx, vn_idx)
                        # se a tupla ja foi armazenada, usa o mesmo indice
                        if key in unique_vertex_map: 
                            indices.append(unique_vertex_map[key])
                        # caso contrário, armazena a tupla e o indice
                        else:
                            vertex = raw_vertex_list[int(vertex_idx) - 1]
                            uv = raw_uv_list[int(uv_idx) - 1]
                            vn = raw_vn_list[int(vn_idx) - 1] if vn_idx is not None else [0.0, 0.0, 0.0]

                            idx = len(unique_vertex_map)
                            unique_vertex_map[key] = idx

                            vertices.extend([*vertex, *uv, *vn])
                            indices.append(idx)

        # Define o contexto como sendo o VAO desse objeto
        glBindVertexArray(self.vao)

        # Envia dados de vértices para GPU
        self.vertices = np.array(vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Envia índices para cada material
        for mat_name, indices in material_indices.items():
            material = self.material_library.get_or_default(mat_name)
            material.setup_ebo(indices)

        # Define o layout dos atributos de vértice no shader
        stride = 8 * self.vertices.itemsize  # 3 (posição) + 2 (uv) + 3 (normais) = 8

        glEnableVertexAttribArray(0)  # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # UV
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * self.vertices.itemsize))

        glEnableVertexAttribArray(2)  # Normais
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(5 * self.vertices.itemsize))
        
        # Limpa o contexto do VAO
        glBindVertexArray(0)

    def _circular_sliding_window_of_three(self, arr: list) -> list:
        if len(arr) == 3:
            return arr
        
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i:i+3])
        return result

    @staticmethod
    def from_path(obj_path: str, default_texture_path: str | None = None) -> "Mesh":
        """
        Se o arquivo .obj já tiver sido carregado, retorna o objeto Mesh
        armazenado em memória. Caso contrário, carrega o arquivo .obj,
        cria um objeto Mesh e armazena ele em memória para uso futuro.
        """
        key = (obj_path, default_texture_path)
        if key not in loaded_meshes:
            loaded_meshes[key] = Mesh(obj_path, default_texture_path)
        return loaded_meshes[key]