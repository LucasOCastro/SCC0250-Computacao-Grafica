from OpenGL.GL import *
import numpy as np
from camera import Camera

class Renderer:
    """
    Classe responsável por gerenciar a renderização OpenGL, incluindo:
    - Compilação de shaders
    - Criação do programa GPU
    - Configuração de estados de renderização
    - Envio de parâmetros
    """
    
    def __init__(self, vert_path: str, frag_path: str):
        # Habilita teste de profundidade
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # Habilita blending para transparência
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Habilita textures
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

        # Cria o programa
        self.program = glCreateProgram()
        
        # Compila os shaders
        self.vertex = self._compile_shader(GL_VERTEX_SHADER, vert_path, 'Vertex Shader')
        self.fragment = self._compile_shader(GL_FRAGMENT_SHADER, frag_path, 'Fragment Shader')

        # Linka o programa e verifica erros
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
        
        # Define este programa como o ativo
        glUseProgram(self.program)
        

    def _compile_shader(self, shader_type: any, shader_path: str, name: str) -> any:
        try:
            with open(shader_path, 'r') as shader_file:
                shader_code = shader_file.read()
        except IOError as e:
            print(f"Erro ao abrir {name}")
            raise e
        
        # Cria e compila o shader
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            print(error)
            raise RuntimeError(f"Erro de compilacao do {name}")
        
        # Anexa o shader ao programa principal
        glAttachShader(self.program, shader)
        return shader
    
    def set_camera(self, camera: Camera) -> None:
        """Define a matriz de visualização e a matriz de projeção a partir de uma câmera."""
        
        view = camera.get_view_matrix()
        self.set_mat4("view", view)

        projection = camera.get_projection_matrix()
        self.set_mat4("projection", projection)

    def set_mat4(self, name: str, value: np.ndarray) -> None:
        # Achata a matriz para formato OpenGL
        value = value.reshape(1,16)
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_TRUE, value)

    def toggle_wireframe(self) -> None:
        if glGetIntegerv(GL_POLYGON_MODE)[0] == GL_FILL:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)