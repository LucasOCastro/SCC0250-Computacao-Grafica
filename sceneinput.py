from scene import Scene
from rendering.renderer import Renderer
from input import Input
import glfw
from matrixmath import *

class SceneInput:
    """
    Classe para manipular a cena de acordo com o input do usuário.
    """
    def __init__(self, scene: Scene, renderer: Renderer, input: Input):
        self.scene = scene
        self.input = input
        self.renderer = renderer

        input.register_key_callback(glfw.KEY_P, renderer.toggle_wireframe)
        self._setup_editable_lights()

    def update(self, delta_time: float) -> None:
        for element in self.scene.container.children:
            element.update(self.input, delta_time)
        
        self._update_editable_lights(delta_time)
    
    def _setup_editable_lights(self):
        # Callbacks de input para controlar as luzes
        def on_light_key_pressed(i):
            print(f"Light {i} selected")
            self.current_light = self.editable_lights[i]
        def on_reset_key_pressed():
            self.current_light.reset()
        
        # Define as teclas para controlar as luzes
        self.key_light_down = glfw.KEY_KP_2
        self.key_light_up = glfw.KEY_KP_8
        self.key_light_reset = glfw.KEY_KP_5
        self.light_delta_speed = 5

        # Pega todas as luzes da cena e defaulta para a ambiente
        self.editable_lights = self.scene.get_all_lights()
        self.current_light = self.editable_lights[0]

        # Registra as callbacks para cada luz
        for i in range(min(len(self.editable_lights), 9)):
            self.input.register_key_callback(glfw.KEY_1 + i, lambda i=i: on_light_key_pressed(i))
        self.input.register_key_callback(self.key_light_reset, on_reset_key_pressed)

    def _update_editable_lights(self, delta_time: float):
        delta = self.input.get_1d_axis(self.key_light_up, self.key_light_down)
        self.current_light.intensity += delta * delta_time * self.light_delta_speed
            
