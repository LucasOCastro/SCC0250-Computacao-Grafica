
import numpy as np
from objects.object import Object
from objects.primitives.cylinder import Cylinder
from objects.primitives.cube import Cube

DARK_GREEN = (0, 80, 0, 1)
LIGHT_GREEN = (0, 120, 0, 1)

class LillyPad(Object):
    def __init__(self, slices=16, length=0.1, radius=0.5):
        super().__init__()
        self.slices = slices
        self.radius = radius
        self.length = length
        base = self._make_base()
        outlines = self._make_outline()
        self.children = [base, *outlines]

    def _make_base(self):
        base = Cylinder(slices=self.slices, length=self.length, radius=self.radius)
        base.set_single_color(DARK_GREEN)
        #base.set_rot_deg(np.array([90, 0, 0]))
        return base
    
    def _make_outline(self):
        # precisa construir um paralepipedo para cada uma das slices + 1
        outlines = []
        angle_step = 2*np.pi / self.slices

        outline_part_size = 2*np.pi*self.radius / self.slices
        for i in range(self.slices):
            #calcula a media entre o atual e o próximo para saber o centro
            x = np.cos(angle_step*i)*self.radius
            z = np.sin(angle_step*i)*self.radius
            xnext = np.cos(angle_step*(i+1))*self.radius
            znext = np.sin(angle_step*(i+1))*self.radius
            xcube = (x + xnext) / 2
            zcube = (z + znext) / 2
            outline_part = Cube(size=1, color=(1.0, 0, 0, 1))
            #
            outline_part.set_scale([outline_part_size, self.length/2, 0.1])
            outline_part.set_pos([xcube, self.length/2, zcube])
            outline_part.set_rot_rad([0,i*angle_step , 0 ])
            outlines.append(outline_part)
          

        return outlines