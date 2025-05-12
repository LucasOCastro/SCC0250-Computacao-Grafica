import glfw
import numpy as np
from window import Window
import functools
from matrixmath import *

class Input:
    """
    Classe para gerenciamento de entrada.
    """
    
    def __init__(self, window: Window) -> None:
        # Arnazena teclas pressionadas
        self.held_keys = set()
        self.key_press_callbacks = {}

        # Inicializa valores de mouse
        self.mouse_pos = np.array(glfw.get_cursor_pos(window.window))
        self.mouse_delta = np.array([0.0, 0.0], dtype=np.float32)
        self.scroll_delta = np.array([0.0, 0.0], dtype=np.float32)

        # Configura callbacks
        glfw.set_key_callback(glfw.get_current_context(), functools.partial(self._key_event))
        glfw.set_cursor_pos_callback(window.window, functools.partial(self._mouse_event))
        glfw.set_scroll_callback(window.window, functools.partial(self._scroll_event))

    def clear_deltas(self) -> None:
        """
        Reseta os deltas de mouse e scroll para zero.
        Este método deve ser chamado no fim de cada ciclo de update de entrada
        para garantir que as deltas não acumulam entre os frames.
        """
        self.mouse_delta = np.array([0.0, 0.0], dtype=np.float32)
        self.scroll_delta = np.array([0.0, 0.0], dtype=np.float32)

    def register_key_callback(self, key: int, callback: callable) -> None:
        """
        Registra uma função de callback para ser chamada quando uma tecla especificada for pressionada.
        """
        if key in self.key_press_callbacks:
            self.key_press_callbacks[key].append(callback)
        else:
            self.key_press_callbacks[key] = [callback]
    
    def is_key_held(self, key: int) -> bool:
        """
        Retorna True se a tecla especificada estiver pressionada.
        """
        return key in self.held_keys

    def get_1d_axis(self, key_pos: int, key_neg: int) -> float:
        """
        Se a tecla positiva estiver pressionada, retorna 1.0. 
        Se a tecla negativa estiver pressionada, retorna -1.0.
        Caso contrário, retorna 0.0.
        """
        axis = 0.0
        if self.is_key_held(key_pos):
            axis += 1.0
        if self.is_key_held(key_neg):
            axis -= 1.0
        return axis

    def get_2d_axis(self, pos_x: int, neg_x: int, pos_y: int, neg_y: int) -> np.array:
        """
        Retorna um vetor 2D com a direção de input do usuário.
        Se a tecla positiva de X estiver pressionada, o valor de X será 1.0.
        Se a tecla negativa de X estiver pressionada, o valor de X será -1.0.
        Mesma coisa para Y.
        O vetor resultante é normalizado.
        """
        axis = np.array([
            self.get_1d_axis(pos_x, neg_x),
            self.get_1d_axis(pos_y, neg_y)
        ])

        norm = np.linalg.norm(axis)
        if norm != 0.0:
            axis /= norm
        return axis
    
    def get_3d_axis(self, pos_x: int, neg_x: int, pos_y: int, neg_y: int, pos_z: int, neg_z: int) -> np.array:
        """
        Retorna um vetor 3D com a direção de input do usuário.
        Se a tecla positiva de X estiver pressionada, o valor de X será 1.0.
        Se a tecla negativa de X estiver pressionada, o valor de X será -1.0.
        Mesma coisa para Y e Z.
        O vetor resultante é normalizado.
        """
        axis = np.array([
            self.get_1d_axis(pos_x, neg_x),
            self.get_1d_axis(pos_y, neg_y),
            self.get_1d_axis(pos_z, neg_z)
        ])

        norm = np.linalg.norm(axis)
        if norm != 0.0:
            axis /= norm
        return axis
    
    ###### Callbacks ######

    def _key_event(self, window, key, scancode, action, mods) -> None:
        # Fecha a janela ao pressionar ESC
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            return
        
        # Registra teclas pressionadas. 
        # Não usamos o "repeat" porque o glfw não reconhece várias teclas simultâneas.
        if action == glfw.PRESS:
            self.held_keys.add(key)
            self._fire_callbacks(key)
        elif action == glfw.RELEASE:
            self.held_keys.discard(key)

    def _mouse_event(self, window, xpos, ypos):
        #Atualiza o movimento do mouse a partir da posição atual e anterior.
        mouse_pos = np.array([xpos, ypos], dtype=np.float32)
        self.mouse_delta = mouse_pos - self.mouse_pos
        self.mouse_pos = mouse_pos

    def _scroll_event(self, window, xoffset, yoffset):
        #Apesar do mouse não ter scroll horizontal, armazenamos x e y por completude.
        self.scroll_delta = np.array([xoffset, yoffset], dtype=np.float32)
    
    def _fire_callbacks(self, key: int) -> None:
        """Chama callbacks para uma tecla específica, se houver algum registrado."""
        if key in self.key_press_callbacks:
            for callback in self.key_press_callbacks[key]:
                callback()