import glfw
import numpy as np
from scene import Scene
import functools

class Input:
    def __init__(self, scene: Scene) -> None:
        self.rotation_speed_slow = 100.0
        self.rotation_speed_fast = 300.0
        
        self.translation_speed_slow = 0.5
        self.translation_speed_fast = 1.0

        self.world_rotation_speed = 100

        self.fast = False

        self.scene = scene
        self.keys_pressed = set()

        # Bind self to the callback
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))

    def update(self, delta_time: float) -> None:
        self.rotation_speed = self.rotation_speed_fast if self.fast else self.rotation_speed_slow
        self.translation_speed = self.translation_speed_fast if self.fast else self.translation_speed_slow

        self._handle_world_input(delta_time)
        self._handle_pad_input(delta_time)
        self._handle_frog_input(delta_time)

    def _key_event(self, window, key, scancode, action, mods) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Toggle fast with left control, or hold shift
        if key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
            self.fast = not self.fast
        elif key == glfw.KEY_LEFT_SHIFT:
            if action == glfw.PRESS:
                self.fast = True
            elif action == glfw.RELEASE:
                self.fast = False
        
        # Track held keys
        # Use a set because 'repeat' does not work for multiple key presses
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)

    def _handle_world_input(self, delta_time: float) -> None:
        scene = self.scene
        
        delta = self.world_rotation_speed * delta_time
        if glfw.KEY_LEFT in self.keys_pressed:
            scene.rotate_scene(delta)
        if glfw.KEY_RIGHT in self.keys_pressed:
            scene.rotate_scene(-delta)

    def _handle_frog_input(self, delta_time: float) -> None:
        frog = self.scene.frog
        if glfw.KEY_Z in self.keys_pressed:
            frog.animate(delta_time)
        if glfw.KEY_X in self.keys_pressed:
            frog.animate(-delta_time)

    def _handle_pad_input(self, delta_time: float) -> None:
        lillypad = self.scene.lillypad
        
        rotation_delta = self.rotation_speed * delta_time
        if glfw.KEY_Q in self.keys_pressed:
            lillypad.rotate_deg(rotation_delta, [0, 1, 0], around_self=True)
        if glfw.KEY_E in self.keys_pressed:
            lillypad.rotate_deg(-rotation_delta, [0, 1, 0], around_self=True)

        translation_direction = np.zeros(3)
        if glfw.KEY_W in self.keys_pressed:
            translation_direction[2] += 1
        if glfw.KEY_S in self.keys_pressed:
            translation_direction[2] -= 1
        if glfw.KEY_A in self.keys_pressed:
            translation_direction[0] -= 1
        if glfw.KEY_D in self.keys_pressed:
            translation_direction[0] += 1
        
        direction_magnitude = np.linalg.norm(translation_direction)
        if direction_magnitude > 0:
            # Make movement relative to world
            inverse_rotation = np.linalg.inv(self.scene.container.local_transformation_matrix)
            translation_direction = (inverse_rotation @ [*translation_direction, 1])[:-1]
            translation_direction[1] = 0

            # Normalize movement direction
            translation_direction /= direction_magnitude

            # Apply movement if won't take lillypad out of water
            translation_delta = translation_direction * self.translation_speed * delta_time
            if (self.scene.floor.are_corners_in_water(lillypad.position + translation_delta, self.scene.lillypad_size)):
                lillypad.translate(translation_delta)