from objects.object import Object
from objects.primitives import *
class Firefly(Object):
    YELLOW_COLOR = (240/255, 255/255, 20/255, 1)
    EYE_GLOW_COLOR = (102/255, 102/255, 0, 1)
    BODY_COLOR = (81/255, 81/255, 75/255, 1)
    WING_COLOR = (0, 0, 0, 0.80)
    def __init__(self, size=0.25):
        super().__init__()
        self.size = size
        self.eye_size = size / 3
        #montando os objetos
        self.body, self.yellow_bulb = self._make_body()
        self.eyes = self._make_eyes()
        self.eye_glows = self._make_eyes_glow()
        self.antennas = self._make_antennas()
        self.legs = self._make_legs()
        self.wings = self._make_wings()
        self.children = [
            self.body,
            self.yellow_bulb,
            self.eyes[0],
            self.eyes[1],
            self.eye_glows[0],
            self.eye_glows[1],
            self.antennas[0],
            self.antennas[1],
            self.legs,
            self.wings
        ]
        #variaveis referentes a animacao
        self.is_moving = False
        self.is_hovering = False
        self.animation_progress = 0
        self.hovering_progress = 0
        
    def _make_body(self):
        #bumbum do vagalume
        yellow_bulb = Cube(size=self.size, color=self.YELLOW_COLOR)
        yellow_bulb.set_scale((0.75, 1, 0.75))
        yellow_bulb.set_pos((0, 0, self.size/2*0.75))
        #corpo principal
        body = Cube(size=self.size, color=self.BODY_COLOR)
        body.set_pos((0, 0, -self.size/2))
        return (body, yellow_bulb)

    def _make_eye(self):
        
        eye_size = self.eye_size
        Eye = Cube(size=eye_size, color=(0,0,0,1))
        Eye.set_scale((1, 1.3, 1))
        return Eye
    def _make_eyes(self):
        #cria os dois olhos
        eyes_list = [self._make_eye() for x in range(2)]

        #posiciona os olhos no corpo
        eyes_list[0].translate((-(self.size/2 - self.eye_size/2 - 0.001), self.size/8, -self.size))
        eyes_list[1].translate(((self.size/2 - self.eye_size/2 - 0.001), self.size/8, -self.size))

        return eyes_list

    def _make_eyes_glow(self):
        eye_glow_left = Cube(size=self.eye_size, color=self.EYE_GLOW_COLOR)
        eye_glow_left.set_scale((0.5,1, 0.1))
        eye_glow_left.set_pos((-self.size/2 + self.eye_size/1.5, self.eye_size/2, -self.size - 1/2*self.eye_size))
        eye_glow_right = Cube(size=self.eye_size, color=self.EYE_GLOW_COLOR)
        eye_glow_right.set_scale((0.5,1, 0.1))
        eye_glow_right.set_pos((self.size/2 - self.eye_size/1.5, self.eye_size/2, -self.size - 1/2*self.eye_size))

        return [eye_glow_left, eye_glow_right]
    

    def _make_antennas(self):
        antenna_left = Cube(size=self.size, color=(0,0,0,1))
        antenna_left.set_scale((0.05, 0.1, 0.4))
        antenna_left.set_pos((-self.size/6, self.size/2  , -1.2*self.size ))
        
        antenna_right = Cube(size=self.size, color=(0,0,0,1))
        antenna_right.set_scale((0.05, 0.1, 0.4))
        antenna_right.set_pos((self.size/6, self.size/2 , -1.2*self.size ))

        return [antenna_left, antenna_right]

    def _make_leg(self):
        leg = Cube(self.size/10, color=(0, 0, 0, 1))
        leg.set_scale((0.8, 6, 0.3))
        leg.set_rot_deg((-7.5, 0, 0))
        return leg
    def _make_legs(self):
        z_pos_list=[-self.size/3*x + self.size/6 for x in range(1,4)]
        legs = Object()
        for i in range(0, 3):
            leg_left = self._make_leg()
            leg_left.set_pos((-self.size/4, -self.size*(4/5), z_pos_list[i]))
            leg_right = self._make_leg()
            leg_right.set_pos((self.size/4, -self.size*(4/5), z_pos_list[i]))
            legs.children.append(leg_left)
            legs.children.append(leg_right)
        return legs

    def _make_wing(self):
        wing = Sphere(radius=self.size/5, color=self.WING_COLOR)
        wing.set_scale((1, 0.1, 5))
        wing.set_rot_deg((-15, 0, 0))
        return wing

    def _make_wings(self):
        x_pos = [-self.size/5, self.size/5]
        wings = Object()
        for x in x_pos:
            wing = self._make_wing()
            wing.set_pos((x, self.size/1.5, 0))
            wings.children.append(wing)
        return wings
    
    #funcao chamada a cada iteração do loop principal
    def animate(self, delta_time):
        if not self.is_moving and not self.is_hovering:
            return
        #flutua de cima para baixo
        y_shift=0
        if self.is_hovering:
            y_shift = np.sin(self.hovering_progress*np.pi*2)*self.size/2
            self.hovering_progress+=0.6*delta_time%1
        hovering_array = np.array([0, y_shift, 0])
        if self.is_moving:
            #rotação em torno de um ponto
            cur_index = int(len(self.movable_points)*self.animation_progress)
            self.set_pos(self.movable_points[cur_index]+hovering_array)
            self.set_rot_rad(self.rotations[cur_index])
            self.animation_progress+= (delta_time*0.30)
            self.animation_progress%=1
        else:
            cur_pos = self.position
            cur_pos+= hovering_array/(self.size*1500)
            self.set_pos(cur_pos)
        
    def move_around_point(self, point : np.ndarray, radius : float, num_of_steps=360):
        #caso point seja uma lista 
        point = np.array(point)
        self.is_moving = True
        self.movable_points = []
        self.rotations = []
        angle_step = np.pi*2/num_of_steps
        #gera os pontos
        for i in range(num_of_steps):
            x, z = np.cos(angle_step*i)*radius, np.sin(angle_step*i)*radius
            pos_shift = np.array([x, 0, z])
            self.movable_points.append(point + pos_shift)
            self.rotations.append(np.array([0, -angle_step*i + np.pi, 0]))            

    def hover(self):
        self.is_hovering = True
        self.hovering_progress = 0