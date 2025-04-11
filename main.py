from window import Window
from input import Input
from sceneinput import SceneInput
from renderer import Renderer
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

    # Cria a cena com todos os objetos, inclinada
    world_rotation_deg = np.array([-30, 0, 0], dtype=np.float32)
    world_rotation_rad = np.deg2rad(world_rotation_deg)
    scene = Scene(renderer, world_rotation_rad=world_rotation_rad)

    # Cria o input para manipular a cena
    input = Input(scene)
    scene_input = SceneInput(scene, renderer, input)


    while not window.should_close():
        window.pre_render()
        delta_time = window.delta_time

        # Atualiza inputs
        input.update(delta_time)
        scene_input.update(delta_time)
        
        scene.render_scene()
        window.post_render()

    scene.container.destroy()
    window.destroy()


if __name__ == "__main__":
    main()
    