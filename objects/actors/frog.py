import numpy as np
from objects.object import Object
from objects.primitives.sphere import Sphere
from objects.primitives.cube import Cube

class Frog(Object):
    MAIN_COLOR = (.1, .9, .1, 1)
    SHADOW_COLOR = (0, .8, 0, 1)
    HIGHLIGHT_COLOR = (.4, 1, .4, 1)

    def __init__(self):
        super().__init__()

        self.body = self._make_body()

        self.head = self._make_head()

        self.right_back_leg = self._make_back_leg(1)
        self.left_back_leg = self._make_back_leg(-1)

        self.right_front_leg = self._make_front_leg(1)
        self.left_front_leg = self._make_front_leg(-1)

        self.children = [
            self.body,
            self.head,
            self.right_back_leg,
            self.left_back_leg,
            self.right_front_leg,
            self.left_front_leg
        ]


    def _make_body(self) -> Cube:
        body = Cube(color=self.MAIN_COLOR)
        body.set_face_color(Cube.TOP, self.HIGHLIGHT_COLOR)
        body.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        body.set_scale([1, 0.5, 1])
        body.set_rot_deg([30, 0, 0])
        body.set_pos([0, 0.15, 0])
        return body
    
    def _make_base_leg_cube(self, side_multiplier) -> Cube:    
        cube = Cube(color=self.MAIN_COLOR)
        inner_side = Cube.LEFT if side_multiplier > 0 else Cube.RIGHT
        outer_side = Cube.RIGHT if side_multiplier > 0 else Cube.LEFT
        cube.set_face_color(Cube.TOP, self.HIGHLIGHT_COLOR)
        cube.set_face_color(outer_side, self.HIGHLIGHT_COLOR)
        cube.set_face_color(inner_side, self.SHADOW_COLOR)
        cube.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        return cube
    
    def _make_back_leg(self, side_multiplier: int) -> Cube:
        leg_upper = self._make_base_leg_cube(side_multiplier)
        leg_upper.set_scale([0.45, 0.6, 0.5])
        leg_upper.set_rot_deg([0, 0, side_multiplier * 20])
        leg_upper.set_pos([0.7 * side_multiplier, 0, .22])
        leg_upper.set_pivot([0, -0.3, 0])

        leg_lower = self._make_base_leg_cube(side_multiplier)
        leg_lower.set_scale([1, .2, 1])
        leg_lower.set_rot_deg([0, side_multiplier * 30, side_multiplier * -20])
        leg_lower.set_pos([.5 * side_multiplier, -.5, -.5])
        leg_upper.children.append(leg_lower)

        return leg_upper

    def _make_front_leg(self, side_multiplier: int) -> Cube:
        leg_upper = self._make_base_leg_cube(side_multiplier)
        leg_upper.set_scale([0.25, 0.7, 0.3])
        leg_upper.set_rot_deg([10, 0, side_multiplier * 10])
        leg_upper.set_pos([0.4 * side_multiplier, 0, -0.45])
        leg_upper.set_pivot([0, -0.3, 0])
        return leg_upper
    
    def _make_head(self) -> Sphere:
        head = Cube(color=self.MAIN_COLOR)
        head.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        head.set_face_color(Cube.TOP, self.HIGHLIGHT_COLOR)
        head.set_face_color(Cube.FRONT, self.HIGHLIGHT_COLOR)
        head.set_scale([0.8, 0.6, 0.45])
        head.set_pos([0, 0.65, -0.5])
        return head