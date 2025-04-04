import glfw
import numpy as np
from scene import Scene
import functools

class Input:
    def __init__(self, scene: Scene, world_up: np.ndarray = np.array([0, 1, 0])) -> None:
        self._delta_time = 0
        self.rotation_speed = 100
        self.scene = scene
        self.world_up = world_up

        # Bind self to the callback
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self.key_event))

    def key_event(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if 'frog' in self.scene.__dict__:
            self.handle_frog_input(key, action)

        if 'lillypad' in self.scene.__dict__:
            self.handle_pad_input(key, action)

    def handle_frog_input(self, key: int, action: int) -> None:
        frog = self.scene.frog
        if key == glfw.KEY_Z and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.animate(self._delta_time)

        if key == glfw.KEY_X and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.animate(-self._delta_time)


    def handle_pad_input(self, key: int, action: int) -> None:
        lillypad = self.scene.lillypad
        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            lillypad.rotate_deg(self.rotation_speed * self._delta_time, self.world_up)

        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            lillypad.rotate_deg(-self.rotation_speed * self._delta_time, self.world_up)


    def set_delta_time(self, delta_time: float) -> None:
        self._delta_time = delta_time