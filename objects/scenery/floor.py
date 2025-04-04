import numpy as np
from objects.object import Object
from objects.primitives import Sphere, Cube

LAND_SIZE = 0.7
WATER_SIZE = 1 - LAND_SIZE 
DIRT_COLOR = (88/255, 57/255, 39/255, 1)
WATER_COLOR = (40/255, 67/255, 160/255, 0.85)
GRASS_COLOR = (17/255, 124/255, 19/255, 1)
class Floor(Object):
    def __init__(self, height=0.5, land_portion=0.7):
        super().__init__()
        self.height = height
        self.land_portion = land_portion
        self.water_portion = 1 - land_portion
        self.children.extend(self._make_land())
        self.children.extend(self._make_water_pond())

    def _make_land(self):
        
        dirt_block = Cube(color=DIRT_COLOR)
        grass_patch = Cube(color=GRASS_COLOR)
        dirt_block.set_scale((self.land_portion, self.height, 1))
        grass_patch.set_scale((self.land_portion, self.height/10, 1))
        dirt_block.set_pos((-self.land_portion/2, -self.height/2, 0))
        #coloca em cima 
        grass_patch.set_pos((-self.land_portion/2, self.height/20, 0))
        return [dirt_block, grass_patch]


    def _make_water_pond(self):
        water_block = Cube(color=WATER_COLOR)
        water_block.set_scale((self.water_portion, self.height, 1))
        water_block.set_pos((self.water_portion/2,-self.height/2 + self.height/10 ,0))
        dirt_bottom = Cube(color=DIRT_COLOR)
        dirt_bottom.set_scale((self.water_portion, self.height/10, 1))
        dirt_bottom.set_pos((self.water_portion/2,-self.height + self.height/20,0))
        return [water_block, dirt_bottom]