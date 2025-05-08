from renderer import Renderer
from objects.object import Object
from objects.meshobject import MeshObject
from objects.actors.Gnome import Gnome
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

        self.frog = MeshObject("assets/frog/frog.obj", "assets/frog/frog.jpg")
        self.frog.set_rot_deg([-90, 0, 0])
        self.frog.set_pos([-20, 0, -50])
        self.frog.set_scale_single(2)
        self.container.children.append(self.frog)

        self.skybox = MeshObject("assets/skybox/skybox.obj", "assets/skybox/skybox.png")
        self.skybox.set_scale_single(1000)
        self.container.children.append(self.skybox)
        
        self.gnomes = []
        self.gnomes.append(Gnome("assets/gnomes/gnome1/gnome.obj", "assets/gnomes/gnome1/gnome.png"))
        self.gnomes[0].set_scale_single(0.1)
        self.container.children.extend(self.gnomes)

    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)