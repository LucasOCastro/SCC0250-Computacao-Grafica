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
    
    def __init__(self) -> None:
        # Arnazena teclas pressionadas
        self.held_keys = set()
        self.key_press_callbacks = {}

        # Configura callback para eventos de teclado
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))    
        
    def _key_event(self, window, key, scancode, action, mods) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Controle da visualização de malha (P para toggle)
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.scene.renderer.toggle_wireframe()
        
        # Rastreamento de teclas pressionadas
        if action == glfw.PRESS:
            self.held_keys.add(key)
            if key in self.key_press_callbacks:
                for callback in self.key_press_callbacks[key]:
                    callback()
        elif action == glfw.RELEASE:
            self.held_keys.discard(key)

    def register_callback(self, key: int, callback: callable) -> None:
        if key in self.key_press_callbacks:
            self.key_press_callbacks[key].append(callback)
        else:
            self.key_press_callbacks[key] = [callback]