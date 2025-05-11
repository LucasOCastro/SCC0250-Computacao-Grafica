# Alunos
# Gustavo Bhering Grande - 12542780
# Lucas Oliveira Castro - 13695059

from window import Window
from OpenGL.GL import *
from input import Input
from sceneinput import SceneInput
from renderer import Renderer
from camera import Camera
from scene import Scene

def main():
    # Cria a janela configurada
    window = Window(1920, 1080, "Bosque")
    if (window.window == None):
        return

    # Cria o renderer com os shaders
    vert_path = "shaders/vert.glsl"
    frag_path = "shaders/frag.glsl"
    renderer = Renderer(vert_path, frag_path)
    camera = Camera(window, 0.1, 20000, 45)

    # Cria a cena com todos os objetos
    scene = Scene(renderer)

    # Cria o input para manipular a cena
    input = Input(window)
    scene_input = SceneInput(scene, renderer, input)

    # sem isso, skybox fica com arestas brancas
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    while not window.should_close():
        window.pre_render()
        delta_time = window.delta_time

        # Atualiza inputs
        input.update()
        camera.update(input, delta_time)
        scene_input.update(delta_time)
        
        renderer.set_camera(camera)
        scene.skybox.set_pos(camera.position)
        scene.render_scene()
        window.post_render()

    scene.container.destroy()
    window.destroy()


if __name__ == "__main__":
    main()
    
