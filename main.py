import glfw
from OpenGL.GL import *
from input import Input
from renderer import Renderer
from scene import Scene
from matrixmath import *


def main():
    window_dim = (1080, 900)
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(*window_dim, "Programa", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    # vsync to cap fps
    glfw.swap_interval(1)

    world_rotation_deg = np.array([-30, 0, 0], dtype=np.float32)
    world_rotation_rad = np.deg2rad(world_rotation_deg)

    vert_path = "shaders/vert.glsl"
    frag_path = "shaders/frag.glsl"
    
    renderer = Renderer(vert_path, frag_path)
    scene = Scene(renderer, world_rotation_rad=world_rotation_rad)
    input = Input(scene)

    glfw.show_window(window)

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

    glfw.terminate()


if __name__ == "__main__":
    main()
    