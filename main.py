import glfw
from OpenGL.GL import *
from input import Input
from renderer import Renderer
from scene import Scene
from matrixmath import *


def main():
    # Configura e inicia a janela
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(1080, 900, "Bosque", None, None)
    glfw.make_context_current(window)
    glfw.show_window(window)
    # Limita a taxa de quadros para o deltaTime funcionar
    glfw.swap_interval(1)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
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


    bg_color = (1.0, 1.0, 1.0, 1.0)
    last_time = 0
    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        input.update(delta_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*bg_color)

        scene.render_scene()

        glfw.swap_buffers(window)
        glfw.poll_events()

    scene.container.destroy()
    glfw.terminate()


if __name__ == "__main__":
    main()
    