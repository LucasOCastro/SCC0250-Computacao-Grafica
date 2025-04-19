import numpy as np
import glm
import glfw
from window import Window
from input import Input
from matrixmath import *

class Camera:
    """
    Classe que representa uma camera 3D.
    """
    def __init__(self, window: Window, near: float, far: float, fov: float):
        self.window = window
        self.near = near
        self.far = far
        self.fov = fov
        
        self.move_speed = 5
        self.move_speed_fast = 10
        self.sensitivity = 4
        self.zoom_speed = 1
        
        self.pitch_range = [-89, 89]
        self.yaw_range = None
        self.fov_range = [1.0, 45.0]

        self.position = np.array([0.0, 15.0, 3.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.set_yaw_pitch(0, 0)

        # Captura o mouse
        glfw.set_input_mode(window.window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    def get_view_matrix(self) -> np.array:
        eye = glm.vec3(self.position)
        center = glm.vec3(self.position + self.forward)
        up = glm.vec3(self.up)
        view = glm.lookAt(eye, center, up)
        return np.array(view)
    
    def get_projection_matrix(self) -> np.array:
        aspect = self.window.width / self.window.height
        projection = glm.perspective(self.fov, aspect, self.near, self.far)
        return np.array(projection)
    
    def set_yaw_pitch(self, yaw: float, pitch: float) -> None:
        """
        Define o angulo de yaw e pitch da camera, atualizando a matriz de rotacao e o vetor forward.
        """
        yaw = self._clamp_to_range(yaw, self.yaw_range)
        pitch = self._clamp_to_range(pitch, self.pitch_range)

        self.yaw = yaw
        self.pitch = pitch

        yaw_rad = np.deg2rad(self.yaw)
        pitch_rad = np.deg2rad(self.pitch)
        self.rotation_matrix = rotation_matrix_y(yaw_rad) @ rotation_matrix_x(pitch_rad)

        forward = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.forward = transform_vector(forward, self.rotation_matrix)

    def update(self, input: Input, delta_time: float) -> None:
        move_axis = input.get_3d_axis(glfw.KEY_D, glfw.KEY_A, glfw.KEY_SPACE, glfw.KEY_LEFT_CONTROL, glfw.KEY_S, glfw.KEY_W)
        fast = input.is_key_held(glfw.KEY_LEFT_SHIFT)
        self._update_movement(move_axis, delta_time, fast)
        self._update_rotation(input.mouse_delta, delta_time)
        self._update_zoom(input.scroll_delta, delta_time)

    def _update_movement(self, move_input: np.array, delta_time: float, fast: bool = False) -> None:
        if move_input[0] == 0.0 and move_input[1] == 0.0 and move_input[2] == 0.0:
            return
        
        move_speed = self.move_speed_fast if fast else self.move_speed

        movement_direction = transform_vector(move_input, self.rotation_matrix)
        movement_delta = movement_direction * move_speed * delta_time
        self.position += movement_delta

    def _update_rotation(self, mouse_delta: np.array, delta_time: float) -> None:
        if mouse_delta[0] == 0.0 and mouse_delta[1] == 0.0:
            return

        rotation_delta = mouse_delta * self.sensitivity * delta_time
        
        yaw = self.yaw - rotation_delta[0] 
        pitch = self.pitch - rotation_delta[1]
        self.set_yaw_pitch(yaw, pitch)

    def _update_zoom(self, scroll_delta: np.array, delta_time: float) -> None:
        if scroll_delta[0] == 0.0 and scroll_delta[1] == 0.0:
            return

        self.fov -= scroll_delta[1] * self.zoom_speed * delta_time
        self.fov = self._clamp_to_range(self.fov, self.fov_range)
        

    def _clamp_to_range(self, value: float, range: list) -> float:
        if range is None:
            return value
        return max(min(value, range[1]), range[0])