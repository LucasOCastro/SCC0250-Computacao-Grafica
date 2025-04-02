import math
import glfw
from OpenGL.GL import *
from input import Input
from renderer import Renderer
from scene import Scene


def main():
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(720, 600, "Programa", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    # vsync to cap fps
    glfw.swap_interval(1)

    vert_path = "shaders/vert.glsl"
    frag_path = "shaders/frag.glsl"
    renderer = Renderer(vert_path, frag_path)
    scene = Scene(renderer)

    input = Input(scene)

    glfw.show_window(window)

    bg_color = (1.0, 1.0, 1.0, 1.0)
    last_time = 0
    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        input.set_delta_time(delta_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*bg_color)

        scene.render_scene()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
    