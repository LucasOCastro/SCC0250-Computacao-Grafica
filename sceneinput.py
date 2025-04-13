from scene import Scene
from renderer import Renderer
from input import Input
import numpy as np
import glfw
from matrixmath import *

class SceneInput:
    """
    Classe para manipular a cena de acordo com o input do usuário.
    """
    def __init__(self, scene: Scene, renderer: Renderer, input: Input):
        self.scene = scene
        self.input = input

        input.register_key_callback(glfw.KEY_P, renderer.toggle_wireframe)

    def update(self, delta_time: float) -> None:
        pass