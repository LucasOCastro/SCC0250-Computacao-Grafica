import numpy as np
from OpenGL.GL import *
from renderer import Renderer
from objects.object import Object
from objects.meshobject import MeshObject
from objects.actors.Gnome import Gnome

class Scene:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.gen_objects();

    def gen_objects(self):
        # Container principal que segura todos os objetos da cena
        self.container = Object()

        self.skybox = MeshObject("skybox/skybox.obj", "skybox.png")
        self.skybox.set_scale_single(1000)
        self.container.children.append(self.skybox)
        
        self.scenario = MeshObject("scenario/scenario.obj")
        self.scenario.set_scale_single(0.4)
        self.scenario.set_pos([0, 0, -50])
        self.container.children.append(self.scenario)

        self.shroom = MeshObject("shroom/shroom.obj", "shroom.png")
        self.shroom.set_rot_deg([0, 90, 0])
        self.shroom.set_pos([0, 0, -50])
        self.container.children.append(self.shroom)

        self.frog = MeshObject("frog/frog.obj", "frog.jpg")
        self.frog.set_rot_deg([-90, 0, 0])
        self.frog.set_pos([-20, 0, -50])
        self.frog.set_scale_single(2)
        self.container.children.append(self.frog)

        self.gnomes = []
        self.gnomes.append(Gnome("gnomes/gnome1/gnome.obj", "gnome.png"))
        self.gnomes[0].set_scale_single(0.1)
        self.container.children.extend(self.gnomes)

    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)