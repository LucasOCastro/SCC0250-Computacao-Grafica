import numpy as np
from objects.object import Object
from objects.primitives import Sphere, Cube

LAND_SIZE = 0.7
WATER_SIZE = 1 - LAND_SIZE 
DIRT_COLOR = (88/255, 57/255, 39/255, 1)
WATER_COLOR = (40/255, 160/255, 40/255, 0.8)
GRASS_COLOR = (17, 124, 19, 1)
class Floor(Object):
    def __init__(self, height=0.5, land_portion=0.7):
        super().__init__()
        self.height = height
        self.land_portion = land_portion
        self.water_portion = 1 - land_portion
    
    def _make_land(self):
        
        dirt_block = Cube(color=DIRT_COLOR)
        grass_patch = Cube(color=GRASS_COLOR)
        dirt_block.set_scale((self.land_portion, self.height, 1))
        grass_patch.set_scale((self.land_portion, self.height/10, 1))
        grass_patch.set_pos()

    def _make_water_pond(self):

