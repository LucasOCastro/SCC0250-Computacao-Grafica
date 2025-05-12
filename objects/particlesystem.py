from objects.object import Object
from objects.meshobject import MeshObject
import numpy as np

class Particle:
    def __init__(self, obj: Object, start_pos: np.ndarray, end_pos: np.ndarray, start_scale: float, end_scale: float, start_rot: np.ndarray, end_rot: np.ndarray, lifetime: float):
        self.obj = obj
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.start_rot = start_rot
        self.end_rot = end_rot
        self.lifetime = lifetime
        self.t = 0
        self.update_transform()


    def update(self, delta_time: float) -> bool:
        """ Returns True if particle should be deleted """
        self.t += delta_time
        self.update_transform()
        return self.t > self.lifetime
    
    def update_transform(self):
        self.obj.set_pos(self.lerp(self.start_pos, self.end_pos))
        self.obj.set_scale_single(self.lerp(self.start_scale, self.end_scale))
        self.obj.set_rot_deg(self.lerp(self.start_rot, self.end_rot))
    
    def lerp(self, a, b):
        return a + (b - a) * (self.t / self.lifetime)


class ParticleSystem(Object):
    def __init__(self, meshes: list[str], radius: float = 1, time_to_spawn: float = 0.5, height_range: tuple[float, float] = [1, 2], lifetime__range: tuple[float, float] = [1, 2], scale_range: tuple[float, float] = [1, 2]):
        super().__init__()

        self.meshes = meshes
        self.active_particles: list[Particle] = []

        self.t = 0
        self.radius = radius
        self.time_to_spawn = time_to_spawn
        self.height_range = height_range
        self.lifetime_range = lifetime__range
        self.scale_range = scale_range
        
        self.active = False

    def update(self, input, delta_time: float):
        self.t += delta_time

        if self.active and self.t > self.time_to_spawn:
            self.t = 0
            rand_mesh = np.random.choice(self.meshes)
            self._spawn_particle(rand_mesh)

        for particle in self.active_particles:
            if particle.update(delta_time):
                self._despawn_particle(particle)

    def _spawn_particle(self, mesh: str):
        start_pos = self._rand_pos_in_circle()
        y_off = np.random.uniform(self.height_range[0], self.height_range[1])
        end_pos = start_pos + np.array([0, y_off, 0], dtype=np.float32)

        start_scale = np.random.uniform(self.scale_range[0], self.scale_range[1])
        end_scale = 0

        start_rot = np.random.uniform(0, 360, size=3)
        end_rot = np.random.uniform(0, 360, size=3)

        lifetime = np.random.uniform(self.lifetime_range[0], self.lifetime_range[1])

        obj = MeshObject(mesh)
        particle = Particle(obj, start_pos, end_pos, start_scale, end_scale, start_rot, end_rot, lifetime)
        self.active_particles.append(particle)
        self.children.append(obj)

    def _despawn_particle(self, particle: Particle):
        self.active_particles.remove(particle)
        self.children.remove(particle.obj)
        particle.obj.destroy()
        

    def _rand_pos_in_circle(self):
        angle = np.random.uniform(0, 2 * np.pi)
        r = self.radius * np.sqrt(np.random.uniform(0, 1))
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        return np.array([x, 0, y], dtype=np.float32)
