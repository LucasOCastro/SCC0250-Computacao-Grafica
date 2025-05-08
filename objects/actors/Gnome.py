import objects.meshobject as meshobject
import glfw
from input import Input
import numpy as np


class Gnome(meshobject.MeshObject):
    def __init__(self, path: str, texture_path: str, gravity = -1, ground_y = 0.0, jump_key = glfw.KEY_U) -> None:
        super().__init__(path, texture_path)
        self.velocity = np.zeros(3, dtype=np.float32)
        self.on_ground = True
        self.ground_y = ground_y
        self.gravity = gravity
        self.jump_key = jump_key
        self.auto_jump = False
        self.will_jump = False
        self.jump_interval = 0.0
    def jump(self, velocity=0.25) -> None:
        #esperando dar o intervalo aleatório do pulo
        if self.on_ground:
            self.will_jump = False
            jump_modifier = np.random.normal(1.30, 0.5)
            jump_modifier = max(0.0, jump_modifier)
            velocity *= jump_modifier
            self.ground_y = self.position[1]
            self.velocity[1] = velocity
            self.on_ground = False

    def stop_on_ground(self) -> None:
        #não cair para fora do chão
        if self.velocity[1] + self.position[1] < self.ground_y:
            self.velocity[1] = 0.0
            self.on_ground = True
            self.set_pos([self.position[0], self.ground_y, self.position[2]])

    def start_jump(self) -> None:
        self.will_jump = True
        self.jump_interval = np.random.random() * 50

    
    def update(self, input : Input, delta_time: float) -> None:
        #detecta para começar o pulo
        if (input.is_key_held(self.jump_key) or self.auto_jump) and self.on_ground and self.will_jump == False:
            self.start_jump()
        if self.will_jump and self.jump_interval <= 0:
            self.jump()
        else:
            self.jump_interval -= delta_time * 100
            

        #aplica velocidade em y
        self.velocity[1] += self.gravity * delta_time
        self.stop_on_ground()
        self.set_pos(self.position + self.velocity)