from renderer import Renderer
from objects.object import Object
from objects.scenery.floor import Floor
from objects.actors.frog import Frog
from objects.actors.lillypad import LillyPad
from objects.actors.tree import Tree
from objects.actors.firefly import Firefly
from matrixmath import *
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer, world_rotation_rad: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.renderer = renderer

        # Inclinação inicial da cena inteira para ficar mais interessante
        self.world_rotation_rad = np.array(world_rotation_rad, dtype=np.float32)
        # Ângulo atual de rotação da cena inteira no eixo y
        self.world_rot_rad = 0

        self.gen_objects();

    def gen_objects(self):
        # Container principal que segura todos os objetos da cena
        self.container = Object()
        self.container.set_rot_rad(self.world_rotation_rad)

        self.floor = Floor()
        self.floor.set_scale([1.5, 1, 1.5])
        self.floor.set_rot_deg([0, 90, 0])
        self.container.children.append(self.floor)
        
        self.lillypad = LillyPad()
        self.lillypad.set_scale_single(.3)
        self.lillypad.set_pos([0, .05, -.25])
        # O tamanho da lillypad para o cálculo de colisão com a borda da água
        self.lillypad_size = np.array([.25, 0, .1])
        self.container.children.append(self.lillypad)

        self.frog = Frog()
        self.frog.set_scale_single(.36)
        self.frog.set_pos([0, .2, 0])
        self.lillypad.children.append(self.frog)

        tree_pos = [0, .3, .4]
        self.tree = Tree()
        self.tree.set_scale_single(.25)
        self.tree.set_pos(tree_pos)
        self.container.children.append(self.tree)

        self.firefly = Firefly(0.05)
        self.firefly.move_around_point(tree_pos, .25, 360)
        self.firefly.hover()
        self.container.children.append(self.firefly)

    def rotate_scene(self, angle_deg: float) -> None:
        self.world_rot_rad += np.deg2rad(angle_deg)
        final_rot_rad = self.world_rotation_rad + np.array([0, self.world_rot_rad, 0])
        self.container.set_rot_rad(final_rot_rad)
    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)