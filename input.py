import glfw
import numpy as np
from window import Window
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
    
    def __init__(self, window: Window) -> None:
        # Arnazena teclas pressionadas
        self.held_keys = set()
        self.key_press_callbacks = {}

        # Inicializa valores de mouse
        self.mouse_pos = np.array([0.0, 0.0], dtype=np.float32)
        self.mouse_delta = np.array([0.0, 0.0], dtype=np.float32)
        self.scroll_delta = np.array([0.0, 0.0], dtype=np.float32)

        # Configura callbacks
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))
        glfw.set_cursor_pos_callback(window.window, functools.partial(self._mouse_event))
        glfw.set_scroll_callback(window.window, functools.partial(self._scroll_event))

    def update(self) -> None:
        self.mouse_delta = np.array([0.0, 0.0], dtype=np.float32)
        self.scroll_delta = np.array([0.0, 0.0], dtype=np.float32)

    def register_key_callback(self, key: int, callback: callable) -> None:
        if key in self.key_press_callbacks:
            self.key_press_callbacks[key].append(callback)
        else:
            self.key_press_callbacks[key] = [callback]
    
    def is_key_held(self, key: int) -> bool:
        return key in self.held_keys

    def get_1d_axis(self, key_pos: int, key_neg: int) -> float:
        if self.is_key_held(key_pos):
            return 1.0
        if self.is_key_held(key_neg):
            return -1.0
        return 0.0

    def get_2d_axis(self, pos_x: int, neg_x: int, pos_y: int, neg_y: int) -> np.array:
        axis = np.array([0.0, 0.0], dtype=np.float32)
        if self.is_key_held(pos_x):
            axis[0] = 1.0
        if self.is_key_held(neg_x):
            axis[0] = -1.0
        if self.is_key_held(pos_y):
            axis[1] = 1.0
        if self.is_key_held(neg_y):
            axis[1] = -1.0
        norm = np.linalg.norm(axis)
        if norm != 0.0:
            axis /= norm
        return axis
    
    def get_3d_axis(self, pos_x: int, neg_x: int, pos_y: int, neg_y: int, pos_z: int, neg_z: int) -> np.array:
        axis = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        if self.is_key_held(pos_x):
            axis[0] = 1.0
        if self.is_key_held(neg_x):
            axis[0] = -1.0
        if self.is_key_held(pos_y):
            axis[1] = 1.0
        if self.is_key_held(neg_y):
            axis[1] = -1.0
        if self.is_key_held(pos_z):
            axis[2] = 1.0
        if self.is_key_held(neg_z):
            axis[2] = -1.0

        norm = np.linalg.norm(axis)
        if norm != 0.0:
            axis /= norm
        return axis
    
    def _key_event(self, window, key, scancode, action, mods) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Rastreamento de teclas pressionadas
        if action == glfw.PRESS:
            self.held_keys.add(key)
            self._fire_callbacks(key)
        elif action == glfw.RELEASE:
            self.held_keys.discard(key)

    def _mouse_event(self, window, xpos, ypos):
        mouse_pos = np.array([xpos, ypos], dtype=np.float32)
        self.mouse_delta = mouse_pos - self.mouse_pos
        self.mouse_pos = mouse_pos

    def _scroll_event(self, window, xoffset, yoffset):
        self.scroll_delta = np.array([xoffset, yoffset], dtype=np.float32)
    
    def _fire_callbacks(self, key: int) -> None:
        if key in self.key_press_callbacks:
            for callback in self.key_press_callbacks[key]:
                callback()