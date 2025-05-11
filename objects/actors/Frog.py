import objects.meshobject as meshobject
import numpy as np
import objects.object as object

class FrogCrowned(object.Object):
    def __init__(self):
        super().__init__()
        self.frog = meshobject.MeshObject("frog/frog.obj", "frog.jpg")
        self.frog.set_rot_deg([-90, 0, 0])
        self.frog.set_scale_single(2)
        self.crown = meshobject.MeshObject("crown/crown.obj", "crown.png")
        self.crown.set_rot_deg([-30, 0, 0])
        self.crown.set_scale_single(2)
        self.crown.set_pos([0, 6, 4])
        self.children.append(self.frog)
        self.children.append(self.crown)