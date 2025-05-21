import numpy as np
from OpenGL.GL import *
from objects.object import Object
from objects.meshobject import MeshObject
from objects.actors.cauldron import Cauldron
from objects.actors.Gnome import Gnome
from objects.actors.Frog import FrogCrowned

class Scene:
    def __init__(self):
        self.gen_objects()

    def gen_objects(self):
        # Container principal que segura todos os objetos da cena
        self.container = Object()

        self.skybox = MeshObject("skybox/skybox.obj", "skybox.png")
        self.skybox.set_scale_single(1000)
        self.skybox.mesh.material_library.get_default().set_filter_mode(GL_NEAREST)
        self.container.add_child(self.skybox)
        
        self.scenario = MeshObject("scenario/scenario.obj")
        self.scenario.set_scale_single(0.4)
        self.scenario.set_pos([0, 0, -50])
        self.container.add_child(self.scenario)

        self.shroom = MeshObject("shroom/shroom_new.obj")
        self.shroom.set_scale_single(5)
        self.shroom.set_rot_deg([0, -100, 0])
        self.shroom.set_pos([0, 0, -50])
        self.container.add_child(self.shroom)

        shroom_floor_height = 3.4
        self.witch = MeshObject("witch/witch.obj")
        self.witch.set_scale_single(6)
        self.witch.set_pos([0, shroom_floor_height, -60])
        self.container.add_child(self.witch)
        
        self.cauldron = Cauldron()
        self.cauldron.set_pos([0, shroom_floor_height, -52])
        self.container.add_child(self.cauldron)

        frog_pos = np.array([-30, 0, -50])
        self.frog = FrogCrowned()
        self.frog.set_pos(frog_pos)
        self.container.add_child(self.frog)
        
        self.frog_house = MeshObject("frog_house/frog_house.obj")
        self.frog_house.set_pos(frog_pos + [0, 0, -30])
        self.frog_house.set_scale_single(8)
        self.container.add_child(self.frog_house)

        GNOMES_NUM = 7
        gnomes = [Gnome("gnomes/gnome1/gnome.obj") for _ in range(GNOMES_NUM)]
        angle_step = 2*np.pi / GNOMES_NUM
        for i, gnome in enumerate(gnomes):
            #posiciona os gnomos em um circulo
            offset = np.array((frog_pos), dtype=np.float32)
            radius = 10
            gnome.set_pos(offset + np.array([np.cos(angle_step* i)*radius, 0, np.sin(angle_step* i)*radius], dtype=np.float32))
            gnome.set_scale_single(0.15)
            #seta a rotacao de modo que o gnome fique olhando para o centro do circulo
            gnome.set_rot_rad([0, -angle_step*i - np.pi/2, 0]) 
        self.gnomes = gnomes
        self.container.add_children(self.gnomes)

