from OpenGL.GL import *
from objects.object import Object
from rendering.mesh import Mesh
from rendering.renderer import Renderer

class MeshObject(Object):
    def __init__(self, obj_sub_dir: str, default_texture_path: str | None = None, is_force_unlit: bool = False):
        super().__init__()
        self.mesh = Mesh.from_path(obj_sub_dir, default_texture_path)
        self.is_force_unlit = is_force_unlit
    
    def render(self, renderer: Renderer):
        super().render(renderer)

        if self.is_force_unlit:
            renderer.set_lit(False)
        
        renderer.render_mesh(self.mesh, self.world_transformation_matrix)

        if self.is_force_unlit:
            renderer.set_lit(True)