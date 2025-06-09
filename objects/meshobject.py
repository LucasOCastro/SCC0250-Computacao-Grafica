from OpenGL.GL import *
from objects.object import Object
from rendering.mesh import Mesh
from rendering.renderer import Renderer
from rendering.litmode import LitMode

class MeshObject(Object):
    def __init__(self, obj_sub_dir: str, default_texture_path: str | None = None, lit_mode: LitMode | None = None):
        super().__init__()
        self.mesh = Mesh.from_path(obj_sub_dir, default_texture_path)
        self.lit_mode = lit_mode
    
    def render(self, renderer: Renderer):
        super().render(renderer)
        renderer.render_mesh(self.mesh, self.world_transformation_matrix, self.lit_mode)