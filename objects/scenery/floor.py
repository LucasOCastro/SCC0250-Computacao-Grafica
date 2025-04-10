import numpy as np
from objects.object import Object
from objects.scenery.grasspatch import GrassPatch
from objects.primitives import Cube
from matrixmath import *

LAND_SIZE = 0.7
WATER_SIZE = 1 - LAND_SIZE 
GRASS_PADDING = np.array([0.08, 0, 0.03])
GRASS_DENSITY = 40
GRASS_Y = 0.05
DIRT_COLOR = (88/255, 57/255, 39/255, 1)
WATER_COLOR = (40/255, 67/255, 160/255, 0.85)
GRASS_COLOR = (0.537, 0.690, 0.290, 1.0)
class Floor(Object):
    def __init__(self, height=0.5, land_portion=0.7):
        super().__init__()
        self.height = height
        self.land_portion = land_portion
        self.water_portion = 1 - land_portion
        self.children.extend(self._make_land())
        self.children.extend(self._make_water_pond())
        self.children.extend(self._make_grass_patch())

    def get_closest_border_local_normal(self, position: np.ndarray) -> np.ndarray:
        """Retorna o vetor normal da borda mais proxima de um ponto dentro da água"""
        local_position = self.world_to_local(position)
        if abs(local_position[0]) > abs(local_position[2]):
            if local_position[0] > self.water_portion / 2:
                return np.array([1, 0, 0])
            else:
                return np.array([-1, 0, 0])
        if local_position[2] > 0:
            return np.array([0, 0, 1])
        else:
            return np.array([0, 0, -1])
            
    def get_closest_border_world_normal(self, position: np.ndarray) -> np.ndarray:
        """Retorna o vetor normal da borda mais proxima de um ponto dentro da água, rotacionado para o mundo"""
        local = self.get_closest_border_local_normal(position)
        rot_mat = rotation_matrix_all(self.rotation)
        normal = transform_vector(local, rot_mat)
        return normal

    def is_in_water(self, position: np.ndarray) -> bool:
        """Verifica se um ponto esta dentro da agua"""
        local_position = self.world_to_local(position)
        return 0 < local_position[0] < self.water_portion and -.5 < local_position[2] < .5
    
    def are_corners_in_water(self, center: np.ndarray, size: np.ndarray) -> bool:
        """Verifica se os 4 cantos do retangulo estao dentro da agua"""
        half_size = size / 2
        bl = [center[0] - half_size[0], 0, center[2] - half_size[2]]
        br = [center[0] + half_size[0], 0, center[2] - half_size[2]]
        tl = [center[0] - half_size[0], 0, center[2] + half_size[2]]
        tr = [center[0] + half_size[0], 0, center[2] + half_size[2]]
        return self.is_in_water(bl) and self.is_in_water(br) and self.is_in_water(tl) and self.is_in_water(tr)
    
    def get_local_water_center(self) -> np.ndarray:
        return np.array([self.water_portion/2, 0, 0])

    def get_world_water_center(self) -> np.ndarray:
        return self.local_to_world(self.get_local_water_center())

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
    
    def _make_grass_patch(self):
        # Começa a graminha no começo da parte de terra
        full_area_start = np.array([-self.land_portion, GRASS_Y, -.5])
        # Acaba a graminha no começo da parte de agua
        full_area_end = np.array([0, GRASS_Y, .5])

        area_start = full_area_start + GRASS_PADDING
        area_end = full_area_end - GRASS_PADDING
        area_size = area_end - area_start

        grass_patch = GrassPatch(area_size, GRASS_DENSITY, GRASS_DENSITY)
        grass_patch.set_pos(area_start + area_size/2)
        return [grass_patch]