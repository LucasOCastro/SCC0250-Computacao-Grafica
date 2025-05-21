# Alunos
# Gustavo Bhering Grande - 12542780
# Lucas Oliveira Castro - 13695059

from window import Window
from OpenGL.GL import *
from input import Input
from sceneinput import SceneInput
from rendering.renderer import Renderer
from rendering.program import Program, LitProgram
from objects.lightsource import LightSource
from objects.meshobject import MeshObject
from camera import Camera
from scene import Scene
from rendering.mesh import loaded_meshes
import numpy as np

def main():
    # Cria a janela configurada
    window = Window(1920, 1080, "Bosque")
    if (window.window == None):
        return

    # Cria o renderer com os shaders
    ambient_light_color = np.array([1, 1, 1], dtype=np.float32)
    lit_program = LitProgram("shaders/lit.vert", "shaders/lit.frag", ambient_light_color)
    unlit_program = Program("shaders/unlit.vert", "shaders/unlit.frag")
    renderer = Renderer(lit_program, unlit_program)
    camera = Camera(window, 0.1, 20000, 45)

    # Cria a cena com todos os objetos
    scene = Scene()

    # Cria o input para manipular a cena
    input = Input(window)
    scene_input = SceneInput(scene, renderer, input)

    # TODO testing light, think of alternative to register_light_source
    scene.test_light = LightSource(np.array([0.8, 0, 0], dtype=np.float32))
    scene.container.add_child(scene.test_light)
    light_pos = scene.frog.position + np.array([0, 10, 0], dtype=np.float32)
    scene.test_light.set_pos(light_pos)
    light_skull = MeshObject("particles/skull1/Skull.obj")
    light_skull.is_force_unlit = True
    light_skull.set_scale_single(20)
    scene.test_light.add_child(light_skull)
    renderer.register_light_source(scene.test_light)

    time = 0
    while not window.should_close():
        window.pre_render()
        delta_time = window.delta_time
        time += delta_time

        # Atualiza inputs
        camera.update(input, delta_time)
        scene_input.update(delta_time)
        input.clear_deltas()
        x = np.cos(time)
        y = np.sin(time)
        scene.test_light.translate(np.array([x, 0, y], dtype=np.float32))
        
        # Renderiza a cena
        scene.skybox.set_pos(camera.position)
        renderer.render_object_hierarchy(scene.container, camera)
        window.post_render()

    for mesh in loaded_meshes.values():
        mesh.destroy()
    scene.container.destroy()
    renderer.destroy()
    window.destroy()


if __name__ == "__main__":
    main()
    
