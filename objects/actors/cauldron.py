from objects.object import Object
from objects.meshobject import MeshObject
import numpy as np

class Cauldron(Object):
    def __init__(self):
        super().__init__()
        self.make_pot()
        self.make_spoon()

    def make_pot(self):
        self.pot = MeshObject("cauldron/cauldron.obj")
        self.pot.set_scale_single(0.6)
        self.children.append(self.pot)

    def make_spoon(self):
        self.spoon = MeshObject("spoon/spoon.obj")
        self.spoon.set_rot_deg([90, 0, 0])
        self.spoon.set_pos([0, 5, 0])
        self.children.append(self.spoon)