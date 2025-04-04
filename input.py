import glfw
import numpy as np
from scene import Scene
import functools

class Input:
    def __init__(self, scene: Scene, rotation_speed: float = 100.0, translation_speed: float = 1.0) -> None:
        self.rotation_speed = rotation_speed
        self.translation_speed = translation_speed

        self.scene = scene
        self.keys_pressed = set()

        # Bind self to the callback
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))

    def update(self, delta_time: float) -> None:
        self._handle_pad_input(delta_time)
        self._handle_frog_input(delta_time)

    def _key_event(self, window, key, scancode, action, mods) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Use a set because 'repeat' does not work for multiple key presses
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)


    def _handle_frog_input(self, delta_time: float) -> None:
        frog = self.scene.frog
        if glfw.KEY_Z in self.keys_pressed:
            frog.animate(delta_time)
        if glfw.KEY_X in self.keys_pressed:
            frog.animate(-delta_time)

    def _handle_pad_input(self, delta_time: float) -> None:
        lillypad = self.scene.lillypad

        trans = self.translation_speed * delta_time
        if glfw.KEY_W in self.keys_pressed:
            self.scene.translate_object(lillypad, np.array([0, 0, trans]))
        if glfw.KEY_S in self.keys_pressed:
            self.scene.translate_object(lillypad, np.array([0, 0, -trans]))
        if glfw.KEY_A in self.keys_pressed:
            self.scene.translate_object(lillypad, np.array([-trans, 0, 0]))
        if glfw.KEY_D in self.keys_pressed:
            self.scene.translate_object(lillypad, np.array([trans, 0, 0]))

        rot = self.rotation_speed * delta_time
        if glfw.KEY_Q in self.keys_pressed:
            self.scene.rotate_object_deg(lillypad, rot)
        if glfw.KEY_E in self.keys_pressed:
            self.scene.rotate_object_deg(lillypad, -rot)

        