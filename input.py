import glfw
import numpy as np
from scene import Scene
import functools

class Input:
    def __init__(self, scene: Scene):
        self.rotation_speed = 100
        self.scene = scene
        

        # Bind self to the callback
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self.key_event))

    def key_event(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if 'frog' in self.scene.__dict__:
            self.handle_frog_input(key, action)

        if 'tree' in self.scene.__dict__:
            self.handle_tree_input(key, action)

    def handle_frog_input(self, key: int, action: int) -> None:
        frog = self.scene.frog
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.rotate_deg(self.rotation_speed * self._delta_time, np.array([0, 1, 0]))

        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.rotate_deg(-self.rotation_speed * self._delta_time, np.array([0, 1, 0]))

        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.animate(self._delta_time)

        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            frog.animate(-self._delta_time)

    def handle_tree_input(self, key: int, action: int) -> None:
        tree = self.scene.tree
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            tree.rotate_deg(self.rotation_speed * self._delta_time, np.array([0, 1, 0]))

        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):    
            tree.rotate_deg(-self.rotation_speed * self._delta_time, np.array([0, 1, 0]))


    def set_delta_time(self, delta_time: float) -> None:
        self._delta_time = delta_time