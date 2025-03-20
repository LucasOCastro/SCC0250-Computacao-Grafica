from OpenGL.GL import *
import numpy as np

class Renderer:
    _bg_color = (1.0, 1.0, 1.0, 1.0)

    def __init__(self, vert_path: str, frag_path: str):
        self.program = glCreateProgram()
        self.vertex = self._compile_shader(GL_VERTEX_SHADER, vert_path, 'Vertex Shader')
        self.fragment = self._compile_shader(GL_FRAGMENT_SHADER, frag_path, 'Fragment Shader')

        # Build program and make default
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
        
        glUseProgram(self.program)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    def _compile_shader(self, shader_type: any, shader_path: str, name: str):
        try:
            with open(shader_path, 'r') as shader_file:
                shader_code = shader_file.read()
        except IOError as e:
            print(f"Erro ao abrir {name}")
            raise e

        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            print(error)
            raise RuntimeError(f"Erro de compilacao do {name}")
        
        glAttachShader(self.program, shader)
        return shader
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT) 
        glClearColor(*self._bg_color)

    def setColor(self, name: str, color: tuple) -> None:
        if len(color) == 3:
            color = (*color, 1.0)
        glUniform4f(glGetUniformLocation(self.program, name), *color)

    def setMat4(self, name: str, value: np.ndarray) -> None:
        if value.shape != (1,16):
            value = value.flatten()
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, value)