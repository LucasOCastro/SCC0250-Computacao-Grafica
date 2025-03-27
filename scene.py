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
        example_cube = Cube((1.0, 0.0, 0.0))
        example_cube.set_scale([0.25, 1.0,  0.1])
        example_cube.set_rot_deg(np.array([0.0, 0.0, 45]))
        example_cube.set_pos(np.array([1.0, 5.0, 0.0]))
        
        return [example_cube]

    def render_scene(self) -> None:
        for obj in self.objects:
            obj.render(np.identity(4, dtype=np.float32), self.renderer)