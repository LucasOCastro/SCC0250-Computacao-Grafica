from renderer import Renderer
from objects.object import Object
from objects.meshobject import MeshObject
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.gen_objects();

    def gen_objects(self):
        # Container principal que segura todos os objetos da cena
        self.container = Object()
        self.container.set_pos([0, 0, 0])

        # self.monstro = MeshObject("assets/monstro/monstro.obj", "assets/monstro/monstro.jpg")
        # self.container.children.append(self.monstro)
        self.shroom = MeshObject("assets/shroom/shroom.obj", "assets/shroom/shroom.png")
        self.shroom.set_rot_deg([0, 90, 0])
        self.shroom.set_pos([0, 0, -50])
        self.container.children.append(self.shroom)
        

    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)