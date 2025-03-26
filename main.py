import math
import glfw
from OpenGL.GL import *
import numpy as np
import glm
from renderer import Renderer
from objects.cube import Cube


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

    example_cube = Cube((1.0, 0.0, 0.0))
    example_cube.set_scale([0.25, 1.0,  0.1])
    example_cube.set_rot_deg(np.array([0.0, 0.0, 45]))
    example_cube.set_pos(np.array([1.0, 5.0, 0.0]))
    renderer.objects.append(example_cube)

    glfw.show_window(window)

    while not glfw.window_should_close(window):
        renderer.render()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
    