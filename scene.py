from renderer import Renderer
from objects.object import Object
from typing import List
from objects.cube import Cube
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.objects: List[Object] = self.gen_objects()

    def gen_objects(self) -> List[Object]:
        red_cube = Cube(single_color=(1, 0, 0, 1))
        red_cube.set_scale([0.25, 0.5,  0.5])
        red_cube.set_rot_deg(np.array([45, 45, 0]))
        red_cube.set_pos(np.array([0.5, 0.0, 0.0]))

        multi_cube = Cube(face_colors=[
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (1, 1, 0, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1),
        ])
        multi_cube.set_scale([0.5, 0.5, 0.9])
        multi_cube.set_rot_deg(np.array([30, 60, 45]))
        multi_cube.set_pos(np.array([-0.5, 0.0, 0.0]))
        
        return [red_cube, multi_cube]

    def render_scene(self) -> None:
        for obj in self.objects:
            obj.render(np.identity(4, dtype=np.float32), self.renderer)