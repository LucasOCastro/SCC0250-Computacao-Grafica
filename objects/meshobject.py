from OpenGL.GL import *
from objects.object import Object
from rendering.mesh import Mesh

class MeshObject(Object):
    def __init__(self, obj_sub_dir: str, default_texture_path: str | None = None):
        super().__init__()
        self.mesh = Mesh.from_path(obj_sub_dir, default_texture_path)
        self.is_force_unlit = False