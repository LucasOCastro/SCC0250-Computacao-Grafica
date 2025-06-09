from objects.meshobject import MeshObject
from objects.object import Object
import glfw
import numpy as np
from objects.lightobject import LightObject
from rendering.lightdata import LightData
from rendering.litmode import LitMode

class Elemental(Object):
    def __init__(self):
        super().__init__()
        self.elemental_mesh = MeshObject("elemental-fire/FireElemental.obj", lit_mode=LitMode.UNLIT)
        self.add_child(self.elemental_mesh)
        self.elemental_mesh.set_scale_single(0.25)
        self.elemental_mesh.set_rot_deg([0, -90, 0])
        teste = MeshObject("particles/skull1/Skull.obj", lit_mode=LitMode.UNLIT)
        teste.set_scale_single(4)
        self.hovering = False
        
        
    
    def update(self, input, delta_time):
        #flutuar
        y_shift = np.sin(glfw.get_time() * self.hovering_frequency*2) * .15
        self.set_pos([self.position[0], self.anchor_y + y_shift, self.position[2]])

    #começa ou para de flutuar
    def hover(self, hovering_frequency: float = 1.0):
        if hovering_frequency <= 0:
            self.hovering = False
            return
        self.hovering = True
        self.anchor_y = self.position[1]
        self.hovering_frequency = hovering_frequency