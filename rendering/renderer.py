from OpenGL.GL import *
import numpy as np
from camera import Camera
from rendering.lightdata import LightData
from rendering.mesh import Mesh
from rendering.materials import LightParameters
from editablevalue import EditableValue

class Renderer:
    """
    Classe responsável por gerenciar a renderização OpenGL,
    delegando a renderização para os programas de shader adequados.
    """
    def __init__(self, vert_path: str, frag_path: str):
        # Cria o programa
        self.program = glCreateProgram()
        if not self.program:
            raise RuntimeError('Error creating program')
        
        # Compila os shaders
        self.vertex = self._compile_shader(GL_VERTEX_SHADER, vert_path, 'Vertex Shader')
        self.fragment = self._compile_shader(GL_FRAGMENT_SHADER, frag_path, 'Fragment Shader')

        # Linka o programa e verifica erros
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
        glUseProgram(self.program)

        # Habilita teste de profundidade
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # Habilita blending para transparência
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Habilita texturas
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

        # Prepara offset de parâmetros
        self.light_param_multipliers = {
            'ka': EditableValue(1, 0, 2, 'Ka Multiplier'),
            'kd': EditableValue(1, 0, 2, 'Kd Multiplier'),
            'ks': EditableValue(1, 0, 2, 'Ks Multiplier'),
            'ns': EditableValue(1, 0, 2, 'Ns Multiplier'),
        }
        self.set_lit(True)

    def toggle_wireframe(self) -> None:
        if glGetIntegerv(GL_POLYGON_MODE)[0] == GL_FILL:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Funções para enviar parâmetros genéricos
    def set_mat4(self, name: str, value: np.ndarray) -> None:
        value = value.reshape(1,16) # Achata a matriz para formato OpenGL
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_TRUE, value)

    def set_int(self, name: str, value: int) -> None:
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def set_float(self, name: str, value: float) -> None:
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_vec3(self, name: str, value: np.ndarray) -> None:
        glUniform3fv(glGetUniformLocation(self.program, name), 1, value)

    # Funções para enviar parâmetros especiais
    def set_camera_uniforms(self, camera: Camera) -> None:
        """Define a matriz de visualização e a matriz de projeção a partir de uma câmera."""
        view = camera.get_view_matrix()
        self.set_mat4("view", view)

        projection = camera.get_projection_matrix()
        self.set_mat4("projection", projection)

        position = camera.position
        self.set_vec3("viewPos", position)
    
    def set_light_uniforms(self, lights: list[LightData]):
        """Define as luzes a serem consideradas na renderização."""
        self.set_int("numLights", len(lights))
        for i in range(len(lights)):
            light = lights[i]
            self.set_vec3(f"lights[{i}].position", light.world_position)
            self.set_vec3(f"lights[{i}].color", light.color)
    
    def set_ambient_light(self, ambient_light: LightData):
        """Define a luz ambiente."""
        self.set_vec3("ambientLightColor", ambient_light.color)
    
    def set_lit(self, lit: bool):
        """Se verdadeiro, objetos consideram luzes. Se falso, objetos são renderizados completamente iluminados."""
        self.set_int("lit", int(lit))

    def render_mesh(self, mesh: Mesh, world_transformation_matrix: np.ndarray):
        """Renderiza um mesh e seus materiais a partir da matriz de transformação."""
        self.set_mat4("model", world_transformation_matrix)
        glBindVertexArray(mesh.vao)
        offsets = self.light_param_multipliers
        for material in mesh.material_library.materials.values():
            params = material.light_parameters
            self.set_vec3('ka', params.ka * offsets['ka'].value)
            self.set_vec3('kd', params.kd * offsets['kd'].value)
            self.set_vec3('ks', params.ks * offsets['ks'].value)
            self.set_float('ns', params.ns * offsets['ns'].value)
            glBindTexture(GL_TEXTURE_2D, material.texture_id)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, material.ebo)
            glDrawElements(GL_TRIANGLES, len(material.indices), GL_UNSIGNED_INT, None)
    
    def destroy(self):
        glDetachShader(self.program, self.vertex)
        glDetachShader(self.program, self.fragment)
        glDeleteShader(self.vertex)
        glDeleteShader(self.fragment)
        glDeleteProgram(self.program)

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