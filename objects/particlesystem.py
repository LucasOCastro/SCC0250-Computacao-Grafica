from objects.object import Object
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
    def __init__(self, particle_objs: list[Object], radius: float = 1, time_to_spawn: float = 0.5, height_range: tuple[float, float] = [1, 2], lifetime__range: tuple[float, float] = [1, 2], scale_range: tuple[float, float] = [1, 2]):
        super().__init__()

        self.active_particles: list[Particle] = []
        self.inactive_particles: list[MeshObject] = particle_objs
        self.children.extend(particle_objs) 

        self.t = 0
        self.radius = radius
        self.time_to_spawn = time_to_spawn
        self.height_range = height_range
        self.lifetime_range = lifetime__range
        self.scale_range = scale_range
        
        self.active = True

        for i in range(10):
            self._spawn_particle(0)

    def update(self, input, delta_time: float):
        self.t += delta_time

        if self.active and self.t > self.time_to_spawn and self.inactive_particles:
            self.t = 0
            rand_index = np.random.randint(0, len(self.inactive_particles))
            self._spawn_particle(rand_index)

        for particle in self.active_particles:
            if particle.update(delta_time):
                particle.obj.set_scale_single(0)
                self.active_particles.remove(particle)
                self.inactive_particles.append(particle.obj)

    def _spawn_particle(self, index: int):
        particle = self.inactive_particles[index]
        self.inactive_particles.remove(particle)

        start_pos = self._rand_pos_in_circle()
        y_off = np.random.uniform(self.height_range[0], self.height_range[1])
        end_pos = start_pos + np.array([0, y_off, 0], dtype=np.float32)

        start_scale = np.random.uniform(self.scale_range[0], self.scale_range[1])
        end_scale = 0

        start_rot = np.random.uniform(0, 360, size=3)
        end_rot = np.random.uniform(0, 360, size=3)

        lifetime = np.random.uniform(self.lifetime_range[0], self.lifetime_range[1])

        particle = Particle(particle, start_pos, end_pos, start_scale, end_scale, start_rot, end_rot, lifetime)
        self.active_particles.append(particle)
        

    def _rand_pos_in_circle(self):
        angle = np.random.uniform(0, 2 * np.pi)
        r = self.radius * np.sqrt(np.random.uniform(0, 1))
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        return np.array([x, 0, y], dtype=np.float32)
