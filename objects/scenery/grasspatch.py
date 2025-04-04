import numpy as np
from objects.object import Object
from objects.meshobject import MeshObject
from objects.primitives import Cube

GRASS_ROT_MIN = 0
GRASS_ROT_MAX = 15
GRASS_SCALE_MIN = np.array([0.01, 0.08, 0.02])
GRASS_SCALE_MAX = np.array([0.01, 0.12, 0.02])
GRASS_POS_OFFSET_RANGE = np.array([0.05, 0, 0.01])
GRASS_COLORS = [
    (0.3647, 0.5294, 0.2118, 1.0),
    (0.5020, 0.6157, 0.2353, 1.0),
    (0.3882, 0.5294, 0.0745, 1.0),
    (0.3686, 0.4039, 0.0902, 1.0)
]


class GrassPatch(Object):
    def __init__(self, area_size: np.ndarray, line_count: int, count_per_line: int):
        super().__init__()

        self.area_size = area_size
        self.line_count = line_count
        self.count_per_line = count_per_line

        #TODO destroy all cubes
        cubes = self._make_grass_cubes()
        if len(cubes) == 0:
            return

        squashed = MeshObject.merge_meshes(cubes)
        self.children.append(squashed)


    def _make_grass_cubes(self):
        area_start = -self.area_size / 2
        area_end = self.area_size / 2

        line_count = self.line_count
        count_per_line = self.count_per_line

        pos_step = self.area_size / count_per_line


        cubes = []
        for i in range(line_count):
            for j in range(count_per_line):
                color = GRASS_COLORS[np.random.randint(0, len(GRASS_COLORS))]
                grass = Cube(color=color)

                rot = np.random.uniform(GRASS_ROT_MIN, GRASS_ROT_MAX)
                grass.set_rot_deg([0, rot, 0])

                scale = np.random.uniform(GRASS_SCALE_MIN, GRASS_SCALE_MAX)
                grass.set_scale(scale)

                pos = area_start + np.array([j * pos_step[0], 0, i * pos_step[2]])
                if (pos[0] > area_end[0] or pos[2] > area_end[2]): 
                    break

                rand_off = np.random.uniform(-GRASS_POS_OFFSET_RANGE, GRASS_POS_OFFSET_RANGE)
                grass.set_pos(pos + rand_off)

                cubes.append(grass)

        return cubes
