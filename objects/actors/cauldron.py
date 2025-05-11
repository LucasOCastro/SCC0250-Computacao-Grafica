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
            Cauldron.RESTING: self.rest_state,
            Cauldron.REST_TO_MOVE: self.rest_to_move_state,
            Cauldron.MOVING: self.moving_state,
            Cauldron.MOVE_TO_REST: self.move_to_rest_state
        }

        self.make_pot()
        self.make_spoon()

    def make_pot(self):
        self.pot = MeshObject("cauldron/cauldron.obj")
        self.pot.set_scale_single(0.6)
        self.children.append(self.pot)

    def make_spoon(self):
        self.spoon = MeshObject("spoon/spoon.obj")
        self.spoon.set_rot_deg([90, 0, 0])
        self.spoon.set_pos(self.spoon_move_center)
        self.children.append(self.spoon)

    def update(self, delta_time: float, input: Input) -> None:
        self.t += delta_time
        self.state_t += delta_time

        self.states[self.state](input)


    """
        ESTADOS
    """
    def rest_state(self, input: Input):
        if input.is_key_held(glfw.KEY_H):
            self.state = Cauldron.REST_TO_MOVE
            self.state_t = 0
            return

        pos = self.get_rest_spoon_pos()
        self.spoon.set_pos(pos)
    
    def rest_to_move_state(self, input: Input):
        if self.state_t > self.transition_time:
            self.state = Cauldron.MOVING
            self.state_t = 0
            return

        rest_pos = self.get_rest_spoon_pos()
        move_pos = self.get_move_spoon_pos()
        pos = rest_pos + (move_pos - rest_pos) * (self.state_t / self.transition_time)
        self.spoon.set_pos(pos)
    
    def moving_state(self, input: Input):
        if input.is_key_held(glfw.KEY_H):
            self.state = Cauldron.MOVE_TO_REST
            self.state_t = 0
            return

        pos = self.get_move_spoon_pos()
        self.spoon.set_pos(pos)

    def move_to_rest_state(self, input: Input):
        if self.state_t > self.transition_time:
            self.state = Cauldron.RESTING
            self.state_t = 0
            return

        move_pos = self.get_move_spoon_pos()
        rest_pos = self.get_rest_spoon_pos()
        pos = move_pos + (rest_pos - move_pos) * (self.state_t / self.transition_time)
        self.spoon.set_pos(pos)
    
    """
        POSIÇÕES
    """

    def get_rest_spoon_pos(self):
        hover_amp = 0.6
        hover_freq = 1
        y_off = hover_amp * np.sin(self.t * hover_freq)
        off = np.array([0, y_off, 0], dtype=np.float32)
        return self.spoon_rest_center + off
        
    def get_move_spoon_pos(self):
        hover_amp = 1
        hover_freq = 3
        move_radius = 1
        move_freq = 2
        x_off = move_radius * np.sin(self.t * move_freq)
        z_off = move_radius * np.cos(self.t * move_freq)
        y_off = hover_amp * np.sin(self.t * hover_freq)
        off = np.array([x_off, y_off, z_off], dtype=np.float32)
        return self.spoon_move_center + off
