import numpy as np
from objects.object import Object
from objects.primitives import Sphere, Cube

class Frog(Object):
    MAIN_COLOR = (.1, .9, .1, 1)
    SHADOW_COLOR = (0, .8, 0, 1)
    HIGHLIGHT_COLOR = (.4, 1, .4, 1)
    THROAT_COLOR = (.9, .5, .1, 1)
    
    ANIMATION_MIN_HEAD_ROTATION = 0
    ANIMATION_MAX_HEAD_ROTATION = 60
    ANIMATION_MIN_HEAD_POSITION = np.array([0, 0.65, -0.5])
    ANIMATION_MAX_HEAD_POSITION = np.array([0, 0.7, -0.3])
    ANIMATION_MIN_THROAT_SCALE = 0
    ANIMATION_MAX_THROAT_SCALE = .8
    ANIMATION_LENGTH = .7

    def __init__(self):
        super().__init__()

        self.throat_animation_progress = 0

        self.body = self._make_body()

        self.head = self._make_head()

        self.right_back_leg = self._make_back_leg(1)
        self.left_back_leg = self._make_back_leg(-1)

        self.right_front_leg = self._make_front_leg(1)
        self.left_front_leg = self._make_front_leg(-1)

        self.throat = self._make_throat()

        self.children = [
            self.body,
            self.head,
            self.right_back_leg,
            self.left_back_leg,
            self.right_front_leg,
            self.left_front_leg,
            self.throat
        ]

    def animate(self, delta_time: float) -> None:
        self.throat_animation_progress += delta_time
        self.throat_animation_progress = max(0, min(self.ANIMATION_LENGTH, self.throat_animation_progress))
        normalized_progress = self.throat_animation_progress / self.ANIMATION_LENGTH

        # Cubic Ease-In-Out 
        if normalized_progress < 0.5:
            normalized_progress = 4 * normalized_progress ** 3
        else:
            normalized_progress = 1 - (-2 * normalized_progress + 2) ** 3 / 2

        new_rot = self.ANIMATION_MIN_HEAD_ROTATION + normalized_progress * (self.ANIMATION_MAX_HEAD_ROTATION - self.ANIMATION_MIN_HEAD_ROTATION)
        self.head.set_rot_deg([new_rot, 0, 0])

        new_pos = self.ANIMATION_MIN_HEAD_POSITION + normalized_progress * (self.ANIMATION_MAX_HEAD_POSITION - self.ANIMATION_MIN_HEAD_POSITION)
        self.head.set_pos(new_pos)

        new_scale = self.ANIMATION_MIN_THROAT_SCALE + normalized_progress * (self.ANIMATION_MAX_THROAT_SCALE - self.ANIMATION_MIN_THROAT_SCALE)
        self.throat.set_scale_single(new_scale)

    def _make_body(self) -> Cube:
        body = Cube(color=self.MAIN_COLOR)
        body.set_face_color(Cube.TOP, self.HIGHLIGHT_COLOR)
        body.set_face_color(Cube.RIGHT, self.HIGHLIGHT_COLOR)
        body.set_face_color(Cube.LEFT, self.HIGHLIGHT_COLOR)
        body.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        body.set_face_color(Cube.BACK, self.SHADOW_COLOR)
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
    

    def _make_eye(self, side_multiplier: int) -> Cube:
        eye = Cube(color=(.9, .9, .9, 1))
        eye.set_scale([0.4, 0.45, 0.1])
        eye.set_pos([0.25 * side_multiplier, 0.2, -0.5])

        pupil = Cube(color=(0, 0, 0, 1))
        pupil.set_scale([0.5, 0.8, 0.2])
        pupil.set_pos([0, 0.02, -0.5])
        eye.children.append(pupil)

        return eye
    
    def _make_head(self) -> Cube:
        head = Cube(color=self.MAIN_COLOR)
        head.set_face_color(Cube.BOTTOM, self.SHADOW_COLOR)
        head.set_face_color(Cube.TOP, self.HIGHLIGHT_COLOR)
        head.set_face_color(Cube.FRONT, self.HIGHLIGHT_COLOR)
        head.set_face_color(Cube.RIGHT, self.HIGHLIGHT_COLOR)
        head.set_face_color(Cube.LEFT, self.HIGHLIGHT_COLOR)
        head.set_scale([0.8, 0.6, 0.45])
        head.set_pos(self.ANIMATION_MIN_HEAD_POSITION)

        left_eye = self._make_eye(-1)
        right_eye = self._make_eye(1)

        head.children.append(left_eye)
        head.children.append(right_eye)

        return head
    
    def _make_throat(self) -> Sphere:
        throat = Sphere(color=self.THROAT_COLOR)
        throat.set_scale_single(self.ANIMATION_MIN_THROAT_SCALE)
        throat.set_pos([0, 0.35, -0.5])
        return throat
