from renderer import Renderer
from objects.object import Object
from typing import List
from objects.scenery.floor import Floor
from objects.actors.frog import Frog
from objects.actors.lillypad import LillyPad
from objects.actors.tree import Tree
from matrixmath import *
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer, world_rotation_rad: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.renderer = renderer
        self.world_rotation_rad = np.array(world_rotation_rad, dtype=np.float32)
        self.world_up = (rotation_matrix_all(self.world_rotation_rad) @ np.array([0, 1, 0, 1], dtype=np.float32))[:-1]

        self.objects: List[Object] = self.gen_objects()

    def gen_objects(self) -> List[Object]:
        self.floor = Floor()
        self.floor.set_scale([1.5, 1, 1.5])
        self.floor.set_rot_rad(self.world_rotation_rad)
        self.floor.rotate_deg(90, [0, 1, 0])
        self.floor.set_pos([0, 0, 0])
        
        self.lillypad = LillyPad()
        self.lillypad.set_scale_single(.3)
        self.lillypad.set_rot_rad(self.world_rotation_rad)
        self.translate_object(self.lillypad, np.array([0, .15, -.5]))

        self.frog = Frog()
        self.frog.set_scale_single(.36)
        self.frog.set_pos([0, .2, 0])
        self.lillypad.children.append(self.frog)
        
        return [self.floor, self.lillypad]
    
    def rotate_object_deg(self, obj: Object, angle_deg: np.ndarray) -> None:
        angle_rad = np.deg2rad(angle_deg)
        self.rotate_object_rad(obj, angle_rad)
    
    def rotate_object_rad(self, obj: Object, angle_rad: np.ndarray) -> None:
        axis = self.world_up
        position = np.array(obj.position) # clone because it will be modified
        obj.translate(-position)
        obj.rotate_rad(angle_rad, axis)
        obj.translate(position)

    def translate_object(self, obj: Object, delta: np.ndarray) -> None:
        delta = [*delta, 1]
        delta = (rotation_matrix_all(self.world_rotation_rad) @ delta)[:-1]
        obj.translate(delta)

    def render_scene(self) -> None:
        for obj in self.objects:
            obj.render(np.identity(4, dtype=np.float32), self.renderer)