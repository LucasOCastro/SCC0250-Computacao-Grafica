from objects.object import Object
from objects.meshobject import MeshObject
from objects.particlesystem import ParticleSystem
from input import Input
import numpy as np
import glfw

class Cauldron(Object):
    """
    Um caldeirão com uma colher animada e um sistema de partículas.
    Usa uma state machine para controlar o comportamento de animação.
    """
    RESTING = 0
    REST_TO_MOVE = 1
    MOVING = 2
    MOVE_TO_REST = 3

    def __init__(self, transition_key = glfw.KEY_C) -> None:
        super().__init__()
        self.transition_key = transition_key
        self.t = 0 # tempo decorrido geral
        self.state_t = 0 # tempo decorrido no estado atual

        self.transition_time = 0.5
        self.spoon_rest_center = np.array([0, 9, 0], dtype=np.float32)
        self.spoon_move_center = np.array([0, 6, 0], dtype=np.float32)
        self.state = Cauldron.RESTING
        self.states = {
            Cauldron.RESTING: self._rest_state,
            Cauldron.REST_TO_MOVE: self._rest_to_move_state,
            Cauldron.MOVING: self._move_state,
            Cauldron.MOVE_TO_REST: self._move_to_rest_state
        }

        self.pot = MeshObject("cauldron/cauldron.obj")
        self.pot.set_scale_single(0.6)
        self.children.append(self.pot)

        self.spoon = MeshObject("spoon/spoon.obj")
        self.spoon.set_pos(self.spoon_move_center)
        self.children.append(self.spoon)
        
        particle_meshes = ["particles/skull1/Skull.obj"]
        self.particle_system = ParticleSystem(particle_meshes, radius=1.5)
        self.particle_system.set_pos([0, 5, 0])
        self.children.append(self.particle_system)
    
    def update(self, input: Input, delta_time: float) -> None:
        super().update(input, delta_time)
        self.t += delta_time
        self.state_t += delta_time
        self.states[self.state](input)

    ### ESTADOS ###

    def _transition_lerp(self, a, b):
        """Interpolação linear para transição de estados"""
        return a + (b - a) * (self.state_t / self.transition_time)

    def _rest_state(self, input: Input):
        """Colher parada flutuando acima do caldeirão. H -> transição para MOVING"""
        if input.is_key_held(self.transition_key):
            self.state = Cauldron.REST_TO_MOVE
            self.state_t = 0
            return

        pos, rot = self._get_rest_spoon_pos_rot()
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)
    
    def _rest_to_move_state(self, input: Input):
        """Transição de REST -> MOVING, média entre os dois estados."""
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

    
    def _move_state(self, input: Input):
        """Colher em movimento dentro do caldeirão. H -> transição para RESTING."""
        self.particle_system.active = True
        if input.is_key_held(self.transition_key):
            self.state = Cauldron.MOVE_TO_REST
            self.state_t = 0
            self.particle_system.active = False
            return

        pos, rot = self._get_move_spoon_pos_rot()
        self.spoon.set_pos(pos)
        self.spoon.set_rot_rad(rot)

    def _move_to_rest_state(self, input: Input):
        """Transição de MOVING -> REST, média entre os dois estados."""
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
    
    ### POSIÇÕES ###

    def _get_rest_spoon_pos_rot(self) -> tuple[np.ndarray, np.ndarray]:
        hover_amp = 0.6
        hover_freq = 1
        rot_freq = 0.5

        rad = (self.t * rot_freq) % 2 * np.pi
        rot = np.array([0, rad, 0], dtype=np.float32)

        y_off = hover_amp * np.sin(self.t * hover_freq)
        off = np.array([0, y_off, 0], dtype=np.float32)
        pos = self.spoon_rest_center + off
        
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


