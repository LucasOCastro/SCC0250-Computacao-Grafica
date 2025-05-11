import numpy as np
from OpenGL.GL import *
from renderer import Renderer
from objects.object import Object
from objects.meshobject import MeshObject
from objects.actors.cauldron import Cauldron

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

        self.shroom = MeshObject("shroom/shroom_new.obj")
        self.shroom.set_scale_single(5)
        self.shroom.set_rot_deg([0, -100, 0])
        self.shroom.set_pos([0, 0, -50])
        self.container.children.append(self.shroom)

        self.witch = MeshObject("witch/witch.obj")
        self.witch.set_scale_single(6)
        self.witch.set_pos([0, 8, -60])
        self.container.children.append(self.witch)
        
        self.cauldron = Cauldron()
        self.cauldron.set_pos([0, 8, -52])
        self.container.children.append(self.cauldron)


    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)