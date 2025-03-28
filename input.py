import glfw
import numpy as np
from objects.actors.frog import Frog
import functools

class Input:
    def __init__(self, frog: Frog):
        self.rotation_speed = 100
        self.frog = frog

        # Bind self to the callback
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self.key_event))

    def key_event(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.frog.rotate_deg(self.rotation_speed * self._delta_time, np.array([0, 1, 0]))

        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.frog.rotate_deg(-self.rotation_speed * self._delta_time, np.array([0, 1, 0]))

        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            self.frog.animate(self._delta_time)

        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            self.frog.animate(-self._delta_time)


    def set_delta_time(self, delta_time: float) -> None:
        self._delta_time = delta_time