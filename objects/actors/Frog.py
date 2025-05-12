import objects.meshobject as meshobject
import numpy as np
import objects.object as object
from input import Input
import glfw
class FrogCrowned(object.Object):
    def __init__(self, increase_key = glfw.KEY_UP, decrease_key=glfw.KEY_DOWN, max_size=1.6, min_size=0.25) -> None:
        super().__init__()
        self.increase_key = increase_key
        self.decrease_key = decrease_key
        self.max_size = max_size
        self.min_size = min_size
        self.objects_scale = 0.5
        self.frog = meshobject.MeshObject("frog/frog.obj", "frog.jpg")
        self.frog.set_rot_deg([-90, 0, 0])
        self.frog.set_scale_single(2)
        self.crown = meshobject.MeshObject("crown/crown.obj", "crown.png")
        self.crown.set_rot_deg([-30, 0, 0])
        self.crown.set_scale_single(2)
        self.crown.set_pos([0, 6, 4])
        self.children.append(self.frog)
        self.children.append(self.crown)
        self.set_scale_single(self.objects_scale)
    def update(self, input : Input, delta_time: float) -> None:
        updated_scale = self.objects_scale
        if input.is_key_held(self.increase_key):
            updated_scale = self.objects_scale + 0.8 * delta_time
            updated_scale = min(updated_scale, self.max_size)
        elif input.is_key_held(self.decrease_key):
            updated_scale = self.objects_scale - 0.8 * delta_time
            updated_scale = max(updated_scale, self.min_size)
        self.objects_scale = updated_scale
        self.set_scale_single(self.objects_scale)
        
