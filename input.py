import glfw
import numpy as np
from scene import Scene
import functools

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
        self.rotation_speed_slow = 100.0
        self.rotation_speed_fast = 300.0
        self.translation_speed_slow = 0.5
        self.translation_speed_fast = 1.0
        self.world_rotation_speed = 100        
        self.fast = False

        # Arnazena teclas pressionadas
        self.keys_pressed = set()

        # Configura callback para eventos de teclado
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))

    def update(self, delta_time: float) -> None:
        # Atualiza velocidades de movimento e rotação de acordo com o estado de self.fast
        self.rotation_speed = self.rotation_speed_fast if self.fast else self.rotation_speed_slow
        self.translation_speed = self.translation_speed_fast if self.fast else self.translation_speed_slow

        # Aplica movimentação
        self._handle_world_input(delta_time)
        self._handle_pad_input(delta_time)
        self._handle_frog_input(delta_time)
        self.scene.firefly.animate(delta_time)
        
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

        # Controle da visualização de malha (P para toggle)
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.scene.renderer.toggle_wireframe()

        
        # Rastreamento de teclas pressionadas
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)

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
        rotation_delta = self.rotation_speed * delta_time
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
            translation_direction = (inverse_transform @ [*translation_direction, 1])[:-1] # Adiciona coord homogenea e depois tira
            translation_direction[1] = 0 # Ignora movimento vertical
            translation_direction /= direction_magnitude # Normaliza

            # Aplica movimento se não vai sair da água
            translation_delta = translation_direction * self.translation_speed * delta_time
            if self.scene.floor.are_corners_in_water(lillypad.position + translation_delta, self.scene.lillypad_size):
                lillypad.translate(translation_delta)