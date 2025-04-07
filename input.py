import glfw
import numpy as np
from scene import Scene
import functools
from matrixmath import *

class Input:
    """
    Classe para gerenciamento de entrada e controle da cena.
    Responsável por:
    - Captura de eventos do teclado
    - Controle de velocidade (normal/rápida)
    - Movimentação de objetos na cena
    """
    
    def __init__(self, scene: Scene) -> None:
        self.scene = scene

        # Se self.fast for True, as velocidades de movimento e rotação serão aumentadas
        self.fast = False

        self.pad_rotation_speed_anim = 35.0
        self.pad_rotation_speed_slow = 100.0
        self.pad_rotation_speed_fast = 300.0
        self.pad_translation_speed_anim = 0.2
        self.pad_translation_speed_slow = 0.5
        self.pad_translation_speed_fast = 1.0

        self.firefly_rotation_speed_anim = 0.15
        self.firefly_rotation_speed_slow = 0.2
        self.firefly_rotation_speed_fast = 0.45

        self.world_rotation_speed = 100        

        # Arnazena teclas pressionadas
        self.keys_pressed = set()

        self.animation_mode = False

        # Configura callback para eventos de teclado
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))

    def update(self, delta_time: float) -> None:
        # Atualiza velocidades de movimento e rotação de acordo com o estado de self.fast
        self.pad_rotation_speed = self.pad_rotation_speed_fast if self.fast else self.pad_rotation_speed_slow
        self.pad_translation_speed = self.pad_translation_speed_fast if self.fast else self.pad_translation_speed_slow
        self.firefly_rotation_speed = self.firefly_rotation_speed_fast if self.fast else self.firefly_rotation_speed_slow

        if self.animation_mode:
            self.pad_rotation_speed = self.pad_rotation_speed_anim
            self.pad_translation_speed = self.pad_translation_speed_anim
            self.firefly_rotation_speed = self.firefly_rotation_speed_anim
            self._handle_pad_animation(delta_time)
            self._handle_frog_animation(delta_time)
            self._handle_firefly_animation(delta_time)
        else:
            self._handle_pad_input(delta_time)
            self._handle_frog_input(delta_time)
            self._handle_firefly_input(delta_time)
        
        self._handle_world_input(delta_time)
        self.scene.firefly.update()
        
    def _key_event(self, window, key, scancode, action, mods) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Controle do modo rápido (CTRL para toggle, SHIFT para hold)
        if key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
            self.fast = not self.fast
        elif key == glfw.KEY_LEFT_SHIFT:
            if action == glfw.PRESS:
                self.fast = True
            elif action == glfw.RELEASE:
                self.fast = False

        # Controle do modo de animação (SPACE para toggle)
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.animation_mode = not self.animation_mode

        # Controle da visualização de malha (P para toggle)
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.scene.renderer.toggle_wireframe()
        
        # Rastreamento de teclas pressionadas
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)

    """
    ------------------- CONTROLE MANUAL -------------------
    """

    def _handle_world_input(self, delta_time: float) -> None:
        """Controla rotação da cena inteira (teclas LEFT/RIGHT)"""
        delta = self.world_rotation_speed * delta_time
        if glfw.KEY_LEFT in self.keys_pressed:
            self.scene.rotate_scene(delta)
        if glfw.KEY_RIGHT in self.keys_pressed:
            self.scene.rotate_scene(-delta)

    def _handle_frog_input(self, delta_time: float) -> None:
        """Controla animação do sapo (teclas Z/X)"""
        frog = self.scene.frog
        if glfw.KEY_Z in self.keys_pressed:
            frog.animate(delta_time)
        if glfw.KEY_X in self.keys_pressed:
            frog.animate(-delta_time)

    def _handle_pad_input(self, delta_time: float) -> None:
        """Controla movimentação da lillypad (teclas WASD para movimento, QE para rotação)"""
        lillypad = self.scene.lillypad
        
        # Rotação
        rotation_delta = self.pad_rotation_speed * delta_time
        if glfw.KEY_Q in self.keys_pressed:
            lillypad.rotate_deg(rotation_delta, [0, 1, 0], around_self=True)
        if glfw.KEY_E in self.keys_pressed:
            lillypad.rotate_deg(-rotation_delta, [0, 1, 0], around_self=True)

        # Movimentação
        translation_direction = np.zeros(3)
        if glfw.KEY_W in self.keys_pressed:
            translation_direction[2] += 1
        if glfw.KEY_S in self.keys_pressed:
            translation_direction[2] -= 1
        if glfw.KEY_A in self.keys_pressed:
            translation_direction[0] -= 1
        if glfw.KEY_D in self.keys_pressed:
            translation_direction[0] += 1
        
        if (direction_magnitude := np.linalg.norm(translation_direction)) > 0:
            # Converte direção para coordenadas do mundo
            inverse_transform = np.linalg.inv(self.scene.container.local_transformation_matrix)
            translation_direction = transform_vector(translation_direction, inverse_transform)
            translation_direction[1] = 0 # Ignora movimento vertical
            translation_direction /= direction_magnitude # Normaliza

            # Aplica movimento se não vai sair da água
            translation_delta = translation_direction * self.pad_translation_speed * delta_time
            if self.scene.floor.are_corners_in_water(lillypad.position + translation_delta, self.scene.lillypad_size):
                lillypad.translate(translation_delta)

    def _handle_firefly_input(self, delta_time: float) -> None:
        """Controla movimentação do vagalume (UP/DOWN para girar ao redor)"""
        firefly = self.scene.firefly
        rotation_delta = self.firefly_rotation_speed * delta_time
        if glfw.KEY_UP in self.keys_pressed:
            firefly.move_around_point(rotation_delta)
        if glfw.KEY_DOWN in self.keys_pressed:
            firefly.move_around_point(-rotation_delta)

    """
    ------------------- ANIMAÇÕES -------------------
    """

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