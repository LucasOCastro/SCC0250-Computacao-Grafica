import math
import glfw
from OpenGL.GL import *
import numpy as np
import glm
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

    vert_path = "shaders/vert.glsl"
    frag_path = "shaders/frag.glsl"
    renderer = Renderer(vert_path, frag_path)
    scene = Scene(renderer)

    glfw.show_window(window)

    bg_color = (1.0, 1.0, 1.0, 1.0)
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT) 
        glClearColor(*bg_color)

        scene.render_scene()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
    