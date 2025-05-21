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

        # ambient color
        self.key_ambient_color_down = glfw.KEY_KP_2
        self.key_ambient_color_up = glfw.KEY_KP_8
        self.key_ambient_color_reset = glfw.KEY_KP_5
        self.key_ambient_color_speed = 5
        input.register_key_callback(self.key_ambient_color_reset, renderer.lit_program.reset_ambient_color)

    def update(self, delta_time: float) -> None:
        for element in self.scene.container.children:
            element.update(self.input, delta_time)
        
        self.handle_ambient_color(delta_time)
    
    def handle_ambient_color(self, delta_time: float):
        color_delta = None
        if self.input.is_key_held(self.key_ambient_color_up):
            color_delta = np.ones(3, dtype=np.float32)
        elif self.input.is_key_held(self.key_ambient_color_down):
            color_delta = -np.ones(3, dtype=np.float32)
            
        if color_delta is not None:
            color = self.renderer.lit_program.ambient_light_color
            color += color_delta * delta_time * self.key_ambient_color_speed
            self.renderer.lit_program.set_ambient_color(color)