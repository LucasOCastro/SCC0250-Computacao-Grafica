import numpy as np
from OpenGL.GL import *
from objects.object import Object
from objects.lightobject import LightObject
from objects.meshobject import MeshObject
from objects.actors.cauldron import Cauldron
from objects.actors.Gnome import Gnome
from objects.actors.Frog import FrogCrowned
from rendering.renderer import Renderer
from rendering.lightdata import LightData
from camera import Camera

class Scene:
    def DEBUG_make_light(self, pos, color) -> LightObject:
        light_obj = LightObject(LightData(color))
        light_obj.set_pos(pos)
        light_mesh = MeshObject("particles/skull1/Skull.obj", is_force_unlit=True)
        light_mesh.set_scale_single(20)
        light_obj.add_child(light_mesh)
        return light_obj

    def __init__(self):
        self.container = Object()
        self.interior_container = self._gen_interior()
        self.exterior_container = self._gen_exterior()
        self.container.add_children([self.interior_container, self.exterior_container])

        # TODO testing light, think of alternative to register_light_source
        light_pos = self.frog.position + np.array([0, 10, 0], dtype=np.float32)
        light1 = self.DEBUG_make_light(light_pos, [0, 1, 1])
        self.exterior_container.add_child(light1)

        light_pos = self.witch.position + np.array([0, 10, 0], dtype=np.float32)
        light2 = self.DEBUG_make_light(light_pos, [1, 0, 0])
        self.interior_container.add_child(light2)

        self.test_light_1 = light1
        self.test_light_2 = light2

        self.ambient_light = LightData([1, 1, 1])
        self.exterior_lights: list[LightData] = [light1.light_data]
        self.interior_lights: list[LightData] = [light2.light_data]
    
    def get_all_lights(self) -> list[LightData]:
        return [self.ambient_light] + self.exterior_lights + self.interior_lights
        
    def render_scene(self, renderer: Renderer, camera: Camera) -> None:
        renderer.set_camera_uniforms(camera)
        renderer.set_ambient_light(self.ambient_light)

        renderer.set_light_uniforms(self.exterior_lights)
        self.exterior_container.render(renderer)

        renderer.set_light_uniforms(self.interior_lights)
        self.interior_container.render(renderer)

    def _gen_shroom_piece(self, obj_sub_dir: str):
        """Separamos a construção do cogumelo entre interior e exterior para lidar com luzes."""
        shroom_piece = MeshObject(obj_sub_dir)
        shroom_piece.set_scale_single(5)
        shroom_piece.set_rot_deg([0, -100, 0])
        shroom_piece.set_pos([0, 0, -50])
        return shroom_piece

    def _gen_interior(self):
        container = Object()

        self.shroom_inner = self._gen_shroom_piece("shroom/shroom_inner.obj")
        container.add_child(self.shroom_inner)

        shroom_floor_height = 3.4
        self.witch = MeshObject("witch/witch.obj")
        self.witch.set_scale_single(6)
        self.witch.set_pos([0, shroom_floor_height, -60])
        container.add_child(self.witch)
        
        self.cauldron = Cauldron()
        self.cauldron.set_pos([0, shroom_floor_height, -52])
        container.add_child(self.cauldron)

        return container
    
    def _gen_exterior(self):
        container = Object()

        self.skybox = MeshObject("skybox/skybox.obj", "skybox.png", is_force_unlit=True)
        self.skybox.set_scale_single(1000)
        self.skybox.mesh.material_library.get_default().set_filter_mode(GL_NEAREST)
        container.add_child(self.skybox)

        self.scenario = MeshObject("scenario/scenario.obj")
        self.scenario.set_scale_single(0.4)
        self.scenario.set_pos([0, 0, -50])
        container.add_child(self.scenario)

        self.shroom_outer = self._gen_shroom_piece("shroom/shroom_outer.obj")
        container.add_child(self.shroom_outer)

        frog_pos = np.array([-30, 0, -50])
        self.frog = FrogCrowned()
        self.frog.set_pos(frog_pos)
        container.add_child(self.frog)
        
        self.frog_house = MeshObject("frog_house/frog_house.obj")
        self.frog_house.set_pos(frog_pos + [0, 0, -30])
        self.frog_house.set_scale_single(8)
        container.add_child(self.frog_house)

        GNOMES_NUM = 7
        gnomes = [Gnome("gnomes/gnome1/gnome.obj") for _ in range(GNOMES_NUM)]
        angle_step = 2*np.pi / GNOMES_NUM
        for i, gnome in enumerate(gnomes):
            #posiciona os gnomos em um circulo
            offset = np.array((frog_pos), dtype=np.float32)
            radius = 10
            gnome.set_pos(offset + np.array([np.cos(angle_step* i)*radius, 0, np.sin(angle_step* i)*radius], dtype=np.float32))
            gnome.set_scale_single(0.15)
            #seta a rotacao de modo que o gnome fique olhando para o centro do circulo
            gnome.set_rot_rad([0, -angle_step*i - np.pi/2, 0]) 
        self.gnomes = gnomes
        container.add_children(gnomes)

        return container
