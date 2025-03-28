import numpy as np
from objects.object import Object
from objects.primitives.sphere import Sphere
from objects.primitives.cube import Cube

class Frog(Object):
    MAIN_COLOR = (.1, .9, .1, 1)
    SHADOW_COLOR = (0, .8, 0, 1)

    def __init__(self):
        super().__init__()

        self.body = self._make_body()

        self.right_back_leg = self._make_back_leg(1)
        self.left_back_leg = self._make_back_leg(-1)

        self.right_front_leg = self._make_front_leg(1)
        self.left_front_leg = self._make_front_leg(-1)

        self.children = [
            self.body, 
            self.right_back_leg,
              self.left_back_leg]


    def _make_body(self) -> Cube:
        body = Cube(color=self.MAIN_COLOR)
        body.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        body.set_scale([1, 0.5, 1])
        body.set_rot_deg([30, 0, 0])
        body.set_pos([0, 0.15, 0])
        return body
    
    def _make_back_leg(self, side_multiplier: int) -> Cube:
        leg_upper = Cube(color=self.MAIN_COLOR)

        inner_side = Cube.LEFT if side_multiplier > 0 else Cube.RIGHT
        leg_upper.set_face_color(inner_side, self.SHADOW_COLOR)
        leg_upper.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        
        leg_upper.set_scale([0.45, 0.6, 0.5])
        leg_upper.set_rot_deg([0, 0, side_multiplier * 20])
        leg_upper.set_pos([0.7 * side_multiplier, 0, .22])
        leg_upper.set_pivot([0, -0.3, 0])
        return leg_upper

    def _make_front_leg(self, side_multiplier: int) -> Cube:
        leg_upper = Cube(color=self.MAIN_COLOR)

        inner_side = Cube.LEFT if side_multiplier > 0 else Cube.RIGHT
        leg_upper.set_face_color(inner_side, self.SHADOW_COLOR)
        leg_upper.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        
        leg_upper.set_scale([0.45, 0.6, 0.5])
        leg_upper.set_rot_deg([0, 0, side_multiplier * 20])
        leg_upper.set_pos([0.7 * side_multiplier, 0, -0.22])
        leg_upper.set_pivot([0, -0.3, 0])
        return leg_upper