from OpenGL.GL import *
import numpy as np
from camera import Camera
from objects.object import Object
from objects.meshobject import MeshObject
from rendering.program import Program, LitProgram
from rendering.materials import Material
from rendering.drawcall import DrawCall

class Renderer:
    """
    Classe responsável por gerenciar a renderização OpenGL,
    delegando a renderização para os programas de shader adequados.
    """

    def __init__(self, lit_program: LitProgram, unlit_program: Program):
        self.lit_program = lit_program
        self.unlit_program = unlit_program

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

    def toggle_wireframe(self) -> None:
        if glGetIntegerv(GL_POLYGON_MODE)[0] == GL_FILL:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    def render_object_hierarchy(self, root: Object, camera: Camera) -> None:
        """
        Renderiza uma hierarquia de objetos, configurando os programas de shader apropriados e realizando
        chamadas de desenho para cada objeto na hierarquia.

        Args:
            root (Object): O objeto raiz da hierarquia a ser renderizada.
            camera (Camera): A câmera usada para definir a visualização e projeção.

        Este método coleta as chamadas de desenho (DrawCalls) para cada objeto na hierarquia que possui 
        malhas e materiais associados, e então renderiza esses objetos usando os programas de shader 
        apropriados (lit ou unlit) com base nos materiais de cada objeto.
        """

        # Coleta materiais para cada shader
        program_draw_calls = self._collect_draw_calls(root)

        # Renderiza todos os objetos
        for program, draw_calls in program_draw_calls.items():
            program.use()
            program.set_camera_uniforms(camera)
            for draw_call in draw_calls:
                program.render_draw_call(draw_call)
    
    def _collect_draw_calls(self, root: Object) -> dict[Program, list[DrawCall]]:
        """
        Coleta DrawCalls para todos os objetos na hierarquia que possuem malhas e materiais associados.
        Retorna:
            Um dicionário mapeando programas de shader (`Program`) para listas de DrawCalls correspondentes.
        """
        lit_draw_calls: list[DrawCall] = []
        unlit_draw_calls: list[DrawCall] = []
        def collect_action(obj: Object):
            if not isinstance(obj, MeshObject):
                return
            mesh = obj.mesh
            # Divide os materiais em lit e unlit
            lit_materials: list[Material] = []
            unlit_materials: list[Material] = []
            for material in mesh.material_library.materials.values():
                if material.is_lit:
                    lit_materials.append(material)
                else:
                    unlit_materials.append(material)
            
            # Cria DrawCalls
            world_transformation_matrix = obj.world_transformation_matrix
            if len(lit_materials) > 0:
                lit_draw_calls.append(DrawCall(mesh, lit_materials, world_transformation_matrix))
            if len(unlit_materials) > 0:
                unlit_draw_calls.append(DrawCall(mesh, unlit_materials, world_transformation_matrix))
        root.collect(collect_action)

        # Mapeia por programa
        return {
            self.lit_program: lit_draw_calls,
            self.unlit_program: unlit_draw_calls
        }
        