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

        frog_pos = [-30, 0, -50]
        self.frog = MeshObject("frog/frog.obj", "frog.jpg")
        self.frog.set_rot_deg([-90, 0, 0])
        self.frog.set_pos(frog_pos)
        self.frog.set_scale_single(2)
        self.container.children.append(self.frog)
        GNOMES_NUM = 6
        gnome1s = [Gnome("gnomes/gnome1/gnome.obj", "gnome.png") for _ in range(GNOMES_NUM)]
        angle_step = 2*np.pi / GNOMES_NUM
        for i, gnome in enumerate(gnome1s):
            #posiciona os gnomos em um circulo
            offset = np.array((frog_pos), dtype=np.float32)
            radius = 10
            gnome.set_pos(offset + np.array([np.cos(angle_step* i)*radius, 0, np.sin(angle_step* i)*radius], dtype=np.float32))
            gnome.set_scale_single(0.15)
            #seta a rotacao de modo que o gnome fique olhando para o centro do circulo
            gnome.set_rot_rad([0, -angle_step*i - np.pi/2, 0]) 
        self.gnomes = []
        self.gnomes.extend(gnome1s)
        self.container.children.extend(self.gnomes)

    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)