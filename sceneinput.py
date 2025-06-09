from scene import Scene
from rendering.renderer import Renderer
from input import Input
import glfw
from matrixmath import *
from editablevalue import BaseEditableValue
from window import Window


class SceneInput:
    """
    Classe para manipular a cena de acordo com o input do usuário.
    """
    def __init__(self, scene: Scene, renderer: Renderer, input: Input, window: Window):
        self.scene = scene
        self.input = input
        self.renderer = renderer
        self.window = window

        input.register_key_callback(glfw.KEY_P, renderer.toggle_wireframe)

        self.current_editable: BaseEditableValue = None
        self.editable_values: list[BaseEditableValue] = []
        self._setup_editables()
        

    def update(self, delta_time: float) -> None:
        for element in self.scene.container.children:
            element.update(self.input, delta_time)
        
        self._update_editables(delta_time)
        
    
    def _setup_editables(self):
        # Callbacks de input
        def on_edit_key_pressed(i):
            self.current_editable = self.editable_values[i]
        def on_reset_key_pressed():
            self.current_editable.reset()

        # Define as teclas
        self.key_edit_up = glfw.KEY_KP_8
        self.key_edit_down = glfw.KEY_KP_2
        self.key_edit_reset = glfw.KEY_KP_5
        self.edit_speed = 5

        # Podemos editar as luzes da cena e os parâmetros de materiais globais
        self.editable_values = [
            *self.scene.editables,
            *self.renderer.light_param_multipliers.values(),
        ]
        self.current_editable = self.editable_values[0]
        
        if len(self.editable_values) > 9:
            raise ValueError("Too many editables")
        
        # Registra as callbacks
        for i in range(min(len(self.editable_values), 9)):
            self.input.register_key_callback(glfw.KEY_1 + i, lambda i=i: on_edit_key_pressed(i))
        self.input.register_key_callback(self.key_edit_reset, on_reset_key_pressed)

    def _update_editables(self, delta_time: float):
        delta_input = self.input.get_1d_axis(self.key_edit_up, self.key_edit_down)
        delta = delta_input * delta_time * self.edit_speed
        self.current_editable.apply_delta(delta)
        self.window.set_debug_info(str(self.current_editable))
            
