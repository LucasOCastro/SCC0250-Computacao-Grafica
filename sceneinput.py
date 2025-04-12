from scene import Scene
from renderer import Renderer
from input import Input
import glfw

class SceneInput:
    def __init__(self, scene: Scene, renderer: Renderer, input: Input):
        self.input = input

        input.register_key_callback(glfw.KEY_P, renderer.toggle_wireframe)

    def update(self, delta_time: float) -> None:
        pass