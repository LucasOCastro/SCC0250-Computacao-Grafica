from objects.object import Object
from objects.meshobject import MeshObject
from input import Input
import numpy as np
import glfw

class Cauldron(Object):
    RESTING = 0
    REST_TO_MOVE = 1
    MOVING = 2
    MOVE_TO_REST = 3

    def __init__(self):
        super().__init__()

        self.t = 0
        self.state_t = 0
        self.transition_time = 0.5
        self.spoon_rest_center = np.array([0, 9, 0], dtype=np.float32)
        self.spoon_move_center = np.array([0, 6, 0], dtype=np.float32)
        self.state = Cauldron.RESTING
        self.states = {
            Cauldron.RESTING: self._rest_state,
            Cauldron.REST_TO_MOVE: self._rest_to_move_state,
            Cauldron.MOVING: self._moving_state,
            Cauldron.MOVE_TO_REST: self._move_to_rest_state
        }

        self.pot = MeshObject("cauldron/cauldron.obj")
        self.pot.set_scale_single(0.6)
        self.children.append(self.pot)

        self.spoon = MeshObject("spoon/spoon.obj")
        self.spoon.set_pos(self.spoon_move_center)
        self.children.append(self.spoon)

    def update(self, delta_time: float, input: Input) -> None:
        self.t += delta_time
        self.state_t += delta_time

        self.states[self.state](input)

    """
        ESTADOS
    """
    def _transition_lerp(self, a, b):
        return a + (b - a) * (self.state_t / self.transition_time)

    def _rest_state(self, input: Input):
        if input.is_key_held(glfw.KEY_H):
            self.state = Cauldron.REST_TO_MOVE
            self.state_t = 0
            return

        pos, rot = self._get_rest_spoon_pos_rot()
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)
    
    def _rest_to_move_state(self, input: Input):
        if self.state_t > self.transition_time:
            self.state = Cauldron.MOVING
            self.state_t = 0
            return

        rest_pos, rest_rot = self._get_rest_spoon_pos_rot()
        move_pos, move_rot = self._get_move_spoon_pos_rot()
        pos = self._transition_lerp(rest_pos, move_pos)
        rot = self._transition_lerp(rest_rot, move_rot)
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)

    
    def _moving_state(self, input: Input):
        if input.is_key_held(glfw.KEY_H):
            self.state = Cauldron.MOVE_TO_REST
            self.state_t = 0
            return

        pos, rot = self._get_move_spoon_pos_rot()
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)

    def _move_to_rest_state(self, input: Input):
        if self.state_t > self.transition_time:
            self.state = Cauldron.RESTING
            self.state_t = 0
            return

        move_pos, move_rot = self._get_move_spoon_pos_rot()
        rest_pos, rest_rot = self._get_rest_spoon_pos_rot()
        pos = self._transition_lerp(move_pos, rest_pos)
        rot = self._transition_lerp(move_rot, rest_rot)
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)
    
    """
        POSIÇÕES
    """

    def _get_rest_spoon_pos_rot(self) -> tuple[np.ndarray, np.ndarray]:
        hover_amp = 0.6
        hover_freq = 1
        rot_freq = 0.5

        y_off = hover_amp * np.sin(self.t * hover_freq)
        off = np.array([0, y_off, 0], dtype=np.float32)
        pos = self.spoon_rest_center + off

        rad = (self.t * rot_freq) % 2 * np.pi
        rot = np.array([0, rad, 0], dtype=np.float32)
        
        return pos, rot
        
    def _get_move_spoon_pos_rot(self):
        hover_amp = 1
        hover_freq = 3
        move_radius = 1
        move_freq = 2

        rad = (self.t * move_freq) % 2 * np.pi
        rot = np.array([0, rad, 0], dtype=np.float32)

        x_off = move_radius * np.sin(rad)
        z_off = move_radius * np.cos(rad)
        y_off = hover_amp * np.sin(self.t * hover_freq)
        off = np.array([x_off, y_off, z_off], dtype=np.float32)
        pos =  self.spoon_move_center + off

        
        return pos, rot


