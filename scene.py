from renderer import Renderer
from objects.object import Object
from typing import List
from objects.primitives import Cube, Sphere
from objects.actors.frog import Frog
import numpy as np

class Scene:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.objects: List[Object] = self.gen_objects()

    def gen_objects(self) -> List[Object]:
        # red_cube = Cube(color=(1, 0, 0, 1))
        # red_cube.set_scale([0.25, 0.5,  0.5])
        # red_cube.set_rot_deg(np.array([45, 45, 0]))
        # red_cube.set_pos(np.array([0.5, 0.0, 0.0]))

        # multi_cube = Cube()
        # multi_cube.set_face_color(Cube.FRONT, (0, 1, 0, 1))
        # multi_cube.set_face_color(Cube.BACK, (0, 0, 1, 1))
        # multi_cube.set_face_color(Cube.LEFT, (1, 1, 0, 1))
        # multi_cube.set_face_color(Cube.RIGHT, (1, 0, 1, 1))
        # multi_cube.set_face_color(Cube.TOP, (0, 1, 1, 1))
        # multi_cube.set_face_color(Cube.BOTTOM, (1, 0, 0, 1))
        # multi_cube.set_scale([0.5, 0.5, 0.9])
        # multi_cube.set_rot_deg(np.array([30, 60, 45]))
        # multi_cube.set_pos(np.array([-0.5, 0.0, 0.0]))

        # the_ball = Sphere(color=(0,1,0,1))
        # the_ball.set_scale([0.25, 0.25, 0.25])

        # return [red_cube, multi_cube, the_ball]

        self.frog = Frog()
        self.frog.set_scale([0.7, .7, .7])
        return [self.frog]

    def render_scene(self) -> None:
        for obj in self.objects:
            obj.render(np.identity(4, dtype=np.float32), self.renderer)