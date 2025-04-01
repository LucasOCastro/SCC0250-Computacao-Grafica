
import numpy as np
from objects.object import Object
from objects.primitives import Cube, Cylinder

DARK_GREEN = (0, 80/255, 0, 1)
LIGHT_GREEN = (127/255, 152/255, 86/255, 1)

class LillyPad(Object):
    def __init__(self, slices=32, length=0.1, radius=0.5):
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
            x = np.cos(angle_step*i)*self.radius*0.99
            z = np.sin(angle_step*i)*self.radius*0.99
            outline_part = Cube(size=1, color=(LIGHT_GREEN))
            #posicionando o paralelepipedo
            outline_part.set_scale([outline_part_size, self.length/2, self.length/8])
            outline_part.rotate_rad( -(np.pi/2+i*angle_step*1.00), [0, 1, 0])
            outline_part.set_pos([x, self.length*0.75 , z])
            #gira a parte em torno da origem e não em torno dela mesma
            outline_part.rotate_rad(angle_step/2, [0, 1, 0])
            
            outlines.append(outline_part)
          

        return outlines