from window import Window
from input import Input
from sceneinput import SceneInput
from renderer import Renderer
from camera import Camera
from scene import Scene
import numpy as np

def main():
    # Cria a janela configurada
    window = Window(1080, 900, "Bosque")
    if (window.window == None):
        return

    # Cria o renderer com os shaders
    vert_path = "shaders/vert.glsl"
    frag_path = "shaders/frag.glsl"
    renderer = Renderer(vert_path, frag_path)
    camera = Camera(window, 0.1, 100, 45)

    # Cria a cena com todos os objetos
    scene = Scene(renderer)

    # Cria o input para manipular a cena
    input = Input(window)
    scene_input = SceneInput(scene, renderer, input)


    while not window.should_close():
        window.pre_render()
        delta_time = window.delta_time

        # Atualiza inputs
        camera.update(input, delta_time)
        scene_input.update(delta_time)
        input.update()
        
        renderer.set_camera(camera)
        scene.render_scene()
        window.post_render()

    scene.container.destroy()
    window.destroy()


if __name__ == "__main__":
    main()
    