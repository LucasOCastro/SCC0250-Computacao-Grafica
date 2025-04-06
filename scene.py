from renderer import Renderer
from objects.object import Object
from typing import List
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
        self.world_rotation_rad = np.array(world_rotation_rad, dtype=np.float32)
        self.world_up = (rotation_matrix_all(self.world_rotation_rad) @ np.array([0, 1, 0, 1], dtype=np.float32))[:-1]

        self.gen_objects();

    def gen_objects(self):
        self.container = Object()
        self.container.set_rot_rad(self.world_rotation_rad)

        self.floor = Floor()
        self.floor.set_scale([1.5, 1, 1.5])
        self.floor.set_rot_deg([0, 90, 0])
        
        self.lillypad = LillyPad()
        self.lillypad.set_scale_single(.3)
        self.lillypad.set_pos([0, .05, -.25])
        # self.lillypad_size = np.array([.3, 0, .3])
        self.lillypad_size = np.array([.25, 0, .1])

        self.frog = Frog()
        self.frog.set_scale_single(.36)
        self.frog.set_pos([0, .2, 0])
        self.lillypad.children.append(self.frog)

        self.tree = Tree()
        self.tree.set_scale_single(.25)
        self.tree.set_pos([0, .3, .4])

        self.container.children.append(self.floor)
        self.container.children.append(self.lillypad)
        self.container.children.append(self.tree)

        self.firefly = Firefly(0.1)
        #self.firefly.set_rot_deg((90, 90, 90))
        self.container.children.append(self.firefly)

    world_rot_rad = 0
    def rotate_scene(self, angle_deg: float) -> None:
        self.world_rot_rad += np.deg2rad(angle_deg)
        final_rot_rad = self.world_rotation_rad + np.array([0, self.world_rot_rad, 0])
        self.container.set_rot_rad(final_rot_rad)
    
    def render_scene(self) -> None:
        self.container.render(np.identity(4, dtype=np.float32), self.renderer)