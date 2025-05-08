from objects.object import Object
import numpy as np
from OpenGL.GL import *
from renderer import Renderer
from matrixmath import *
from PIL import Image
from input import Input

class MeshObject(Object):
    def __init__(self, model_path: str, texture_path: str):
        super().__init__()

        # Criação dos buffers VAO, VBO e EBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        # Carrega model e texture
        self._load_model(model_path)
        self._load_texture(texture_path)

        error = glGetError()
        if error != GL_NO_ERROR:
            print(error)
            raise Exception("OpenGL error when creating object")

    def render(self, parent_transformation_matrix: np.ndarray, renderer: Renderer) -> None:
        # Super propaga a renderização para os filhos
        super().render(parent_transformation_matrix, renderer)

        # Atualiza matriz de transformação no shader
        world_mat = np.dot(parent_transformation_matrix, self.model_matrix)
        renderer.set_mat4('model', world_mat)

        # Atualiza textura no shader
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Desenha a mesh
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def destroy(self):
        super().destroy()
        
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        glDeleteBuffers(1, [self.ebo])
        glDeleteTextures([self.texture_id])

    def _load_model(self, model_path: str) -> None:
        raw_vertex_list = []
        raw_uv_list = []
        
        vertices = []
        indices = []
        unique_vertex_map = {}

        with open(model_path, "r") as file:
            for line in file:
                # ignora comentarios e linhas vazias
                if line.startswith('#'): 
                    continue
                values = line.split()
                if not values:
                    continue

                ### recuperando vertices
                if values[0] == 'v':
                    raw_vertex_list.append(values[1:4])
                ### recuperando coordenadas de textura
                elif values[0] == 'vt':
                    raw_uv_list.append(values[1:3])
                ### recuperando faces 
                elif values[0] == 'f':
                    face = self._circular_sliding_window_of_three(values[1:])
                    for v in face:
                        # no .obj uma face é definida por indice_vertice/indice_vt/material
                        # nesse trabalho não usaremos material
                        parts = v.split('/')
                        if len(parts) == 1:
                            raise Exception("Face sem coordenada de textura")

                        vertex_idx = int(parts[0])
                        uv_idx = int(parts[1])

                        # índices negativos são do fim da lista
                        if vertex_idx < 0: 
                            vertex_idx += len(raw_vertex_list) + 1
                        if uv_idx < 0:
                            uv_idx += len(raw_uv_list) + 1

                        # mantemos unicidade dos pares vertice/uv
                        key = (vertex_idx, uv_idx)
                        if key in unique_vertex_map:
                            indices.append(unique_vertex_map[key])
                        else:                            
                            vertex = raw_vertex_list[int(vertex_idx) - 1]
                            uv = raw_uv_list[int(uv_idx) - 1]

                            idx = len(unique_vertex_map)
                            unique_vertex_map[key] = idx

                            vertices.extend([*vertex, *uv])
                            indices.append(idx)

        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        
        # Define o contexto como sendo o VAO desse objeto
        glBindVertexArray(self.vao)

        # Envia dados de vértices para GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Envia índices para GPU
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Define o layout dos atributos de vértice no shader
        stride = 5 * self.vertices.itemsize  # 3 (posição) + 2 (uv) = 5

        glEnableVertexAttribArray(0)  # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # UV
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * self.vertices.itemsize))
        
        # Limpa o contexto do VAO
        glBindVertexArray(0)

    def _load_texture(self, texture_path: str) -> None:
        self.texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        img = Image.open(texture_path)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #image_data = np.array(list(img.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    def _circular_sliding_window_of_three(self, arr: List) -> List:
        if len(arr) == 3:
            return arr
        
        circular_arr = arr + [arr[0]]
        result = []
        for i in range(len(circular_arr) - 2):
            result.extend(circular_arr[i:i+3])
        return result
    
    def update(self, input : Input, delta_time: float) -> None:
       pass