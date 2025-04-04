from renderer import Renderer
from objects.object import Object
from typing import List
from objects.actors.frog import Frog
from objects.actors.tree import Tree
from objects.actors.lillypad import LillyPad
from matrixmath import *
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer, world_rotation_rad: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.renderer = renderer
        self.world_rotation_rad = np.array(world_rotation_rad, dtype=np.float32)
        self.objects: List[Object] = self.gen_objects()

    def gen_objects(self) -> List[Object]:
        self.lillypad = LillyPad()
        self.lillypad.set_scale_single(.3)
        self.lillypad.set_rot_rad(self.world_rotation_rad)

        self.frog = Frog()
        self.frog.set_scale_single(.36)
        self.frog.set_pos([0, .2, 0])
        self.lillypad.children.append(self.frog)
        
        return [self.lillypad]


    def render_scene(self) -> None:
        for obj in self.objects:
            obj.render(np.identity(4, dtype=np.float32), self.renderer)