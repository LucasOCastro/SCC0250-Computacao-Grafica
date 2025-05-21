from OpenGL.GL import *
import numpy as np
from camera import Camera
from objects.lightsource import LightSource
from rendering.mesh import Mesh
from rendering.materials import Material
from rendering.drawcall import DrawCall

class Program:
    """
    Um programa de shader é um par de shaders de vértice e fragmento.
    
    Nesta classe, armazenamos o identificador do programa, bem como os
    identificadores dos shaders que o compõem. Além disso, implementamos
    métodos para compilar e linkar os shaders, e para setar o programa como
    o atual.
    """
    _current_program: 'Program' = None

    def __init__(self, vert_path: str, frag_path: str):
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
        
        # Anexa o shader ao programa
        glAttachShader(self.program, shader)
        return shader
    
    def use(self) -> None:
        # Só chama glUseProgram se o programa atual for diferente
        if Program._current_program != self:
            glUseProgram(self.program)
            Program._current_program = self

    # Funções para enviar parâmetros genéricos
    def set_mat4(self, name: str, value: np.ndarray) -> None:
        self.use()
        value = value.reshape(1,16) # Achata a matriz para formato OpenGL
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_TRUE, value)

    def set_float(self, name: str, value: float) -> None:
        self.use()
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_vec3(self, name: str, value: np.ndarray) -> None:
        self.use()
        glUniform3fv(glGetUniformLocation(self.program, name), 1, value)

    # Funções para enviar parâmetros específicos
    def set_camera_uniforms(self, camera: Camera) -> None:
        """Define a matriz de visualização e a matriz de projeção a partir de uma câmera."""
        view = camera.get_view_matrix()
        self.set_mat4("view", view)

        projection = camera.get_projection_matrix()
        self.set_mat4("projection", projection)
    
    def render_draw_call(self, draw_call: DrawCall):
        """Desenha um DrawCall, aplicando a transformação de mundo, bindando a malha e textura e chamando o glDrawElements."""
        self.set_mat4("model", draw_call.world_transformation_matrix)
        self._bind_mesh(draw_call.mesh)
        for material in draw_call.materials:
            self._bind_material(material)
            glDrawElements(GL_TRIANGLES, len(material.indices), GL_UNSIGNED_INT, None)
        
    def _bind_mesh(self, mesh: Mesh):
        glBindVertexArray(mesh.vao)
    
    def _bind_material(self, material: Material):
        glBindTexture(GL_TEXTURE_2D, material.texture_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, material.ebo)

class LitProgram(Program):
    """
    Programa de shader  específico para nossas shader lit, para renderizar objetos iluminados.
    """
    
    def __init__(self, vert_path: str, frag_path: str, 
                 ambient_color: np.ndarray, 
                 min_ambient_light = 0, 
                 max_ambient_light = 1.5):
        super().__init__(vert_path, frag_path)
        
        self.min_ambient_light = min_ambient_light
        self.max_ambient_light = max_ambient_light
        self.default_ambient_color = ambient_color
        self.set_ambient_color(ambient_color)

    def set_ambient_color(self, color: np.ndarray):
        self.ambient_light_color = np.clip(color, self.min_ambient_light, self.max_ambient_light)
        self.set_vec3('ambientLightColor', self.ambient_light_color)

    def reset_ambient_color(self):
        self.set_ambient_color(self.default_ambient_color)
    

    def set_camera_uniforms(self, camera: Camera):
        super().set_camera_uniforms(camera)
        self.set_vec3("viewPos", camera.position)
    
    def render_draw_call(self, draw_call: DrawCall):
        self._set_light_uniforms(draw_call.lights)
        super().render_draw_call(draw_call)
    
    def _set_light_uniforms(self, lights: list[LightSource]):
        for i in range(len(lights)):
            light = lights[i]
            self.set_vec3(f"lights[{i}].position", light.world_position)
            self.set_vec3(f"lights[{i}].color", light.color)

    def _bind_material(self, material: Material):
        super()._bind_material(material)
        
        lighting_params = material.light_parameters
        keys = ['kd', 'ks', 'ka', 'ns']
        for key in keys:
            if key in lighting_params:
                if isinstance(lighting_params[key], np.ndarray):
                    self.set_vec3(key, lighting_params[key])
                else:
                    self.set_float(key, lighting_params[key])
                
