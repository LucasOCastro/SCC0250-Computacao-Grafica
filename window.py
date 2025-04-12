import glfw
from OpenGL.GL import *

class Window:
    """
    Classe que representa e configura a janela do glfw.
    """
    def __init__(self, width: int, height: int, title: str, bg_color: tuple=(1.0, 1.0, 1.0, 1.0)):
        self.width = width
        self.height = height
        self.title = title
        self.bg_color = bg_color
        
        self._last_time = 0
        self.delta_time = 0

        self._init_window()

    def _init_window(self) -> None:
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
        
        window = glfw.create_window(self.width, self.height, self.title, None, None)
        if (window == None):
            print("Failed to create GLFW window")
            glfw.terminate()

        self.window = window
        glfw.make_context_current(window)
        glfw.show_window(window)

        # Limita a taxa de quadros para o deltaTime funcionar
        glfw.swap_interval(1)

    def should_close(self) -> bool:
        return glfw.window_should_close(self.window)

    def pre_render(self) -> None:
        """ 
        Prepara a janela para renderizar, atualizando o delta_time e limpando a tela com a cor de fundo.
        """
        current_time = glfw.get_time()
        self.delta_time = current_time - self._last_time
        self._last_time = current_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*self.bg_color)

    def post_render(self) -> None:
        """ 
        Finaliza a renderização da janela, trocando os buffers e processando os eventos.
        """
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def destroy(self) -> None:
        glfw.destroy_window(self.window)
        glfw.terminate()