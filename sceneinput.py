from scene import Scene
from renderer import Renderer
from input import Input
import numpy as np
import glfw
from matrixmath import *

class SceneInput:
    def __init__(self, scene: Scene, renderer: Renderer, input: Input):
        self.scene = scene
        self.input = input
        self.animating = True

        self.pad_rotation_speed = 35.0
        self.pad_translation_speed = 0.2
        self.firefly_rotation_speed = 0.15

        input.register_key_callback(glfw.KEY_P, renderer.toggle_wireframe)
        input.register_key_callback(glfw.KEY_T, self._toggle_animating)

    def update(self, delta_time: float) -> None:
        self.scene.firefly.update()
        if self.animating:
            self._animate(delta_time)
        pass


    """
    ------------------- ANIMAÇÕES -------------------
    """
    def _toggle_animating(self) -> None:
        self.animating = not self.animating

    def _animate(self, delta_time: float) -> None:
        self._handle_firefly_animation(delta_time)
        self._handle_pad_animation(delta_time)
        self._handle_frog_animation(delta_time)

    def _handle_frog_animation(self, delta_time: float) -> None:
        """Animação automática do sapo, usando uma state machine simples para animar em intervalos aleatórios."""
        time_between_range = [.2, 5]
        frog = self.scene.frog

        if '_last_frog_animation' not in self.__dict__:
            self._last_frog_animation = 0
        if '_current_frog_interval' not in self.__dict__:
            self._current_frog_interval = np.random.uniform(*time_between_range)
        if '_frog_state' not in self.__dict__:
            self._frog_state = 'idle'
        
        # Se já deu o tempo do intervalo, começa a animação
        if self._frog_state == 'idle' and glfw.get_time() - self._last_frog_animation >= self._current_frog_interval:
            self._frog_state = 'animating_up'
        
        # Se está animando, passa o delta_time pro sapo. Se acabou, começa a animação de volta.
        if self._frog_state == 'animating_up':
            if frog.throat_animation_progress < frog.ANIMATION_LENGTH:
                frog.animate(delta_time)
            else:
                self._frog_state = 'animating_down'

        # Se está animando, passa o delta_time pro sapo. Se acabou, volta para idle e atualiza o intervalo.
        if self._frog_state == 'animating_down':
            if frog.throat_animation_progress > 0:
                frog.animate(-delta_time)
            else:
                self._frog_state = 'idle'
                self._last_frog_animation = glfw.get_time()
                self._current_frog_interval = np.random.uniform(*time_between_range)

    def _handle_pad_animation(self, delta_time: float) -> None:
        """Movimentação automática da lillypad, rotacionando e quicando pelas bordas com tratamento para não ficar preso."""
        if '_current_movement_dir' not in self.__dict__:
            angle = np.random.uniform(0, 2 * np.pi)
            self._current_movement_dir = np.array([np.cos(angle), 0, np.sin(angle)])

        lillypad = self.scene.lillypad
        
        # Quicando nas paredes
        translation_delta = self._current_movement_dir * self.pad_translation_speed * delta_time
        next_pos = lillypad.position + translation_delta
        if not self.scene.floor.are_corners_in_water(next_pos, self.scene.lillypad_size):
            # Reflete a direção em relação à normal
            normal = self.scene.floor.get_closest_border_world_normal(next_pos)
            new_dir = self._current_movement_dir - 2 * np.dot(self._current_movement_dir, normal) * normal

            # Rotaciona levemente para evitar ficar preso
            rand_angle = np.random.uniform(-np.pi / 2, np.pi / 2)
            new_dir = transform_vector(new_dir, rotation_matrix_y(rand_angle))

            # Se a nova direção ainda levar pra fora, aponta pro centro
            next_estimnated_pos = lillypad.position + new_dir * self.pad_translation_speed * delta_time
            if not self.scene.floor.are_corners_in_water(next_estimnated_pos, self.scene.lillypad_size):
                center = self.scene.floor.get_world_water_center()
                new_dir = center - lillypad.position
                new_dir[1] = 0
                new_dir = new_dir / np.linalg.norm(new_dir)

            self._current_movement_dir = new_dir

            # Recalcula depois de quicar
            translation_delta = self._current_movement_dir * self.pad_translation_speed * delta_time

        lillypad.translate(translation_delta)

        # Rotação constante
        rotation_delta = self.pad_rotation_speed * delta_time
        lillypad.rotate_deg(rotation_delta, [0, 1, 0], around_self=True)

    def _handle_firefly_animation(self, delta_time: float) -> None:
        """Movimentação automática do vagalume."""
        firefly = self.scene.firefly
        firefly.move_around_point(delta_time * self.firefly_rotation_speed)