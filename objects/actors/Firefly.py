from objects.object import Object
from objects.meshobject import MeshObject
from objects.lightobject import LightObject
from rendering.lightdata import LightData
from editablevalue import EditableValueGroup, EditableValue
from rendering.litmode import LitMode
import numpy as np
import glfw

class Firefly(Object):
    def __init__(self):
        super().__init__()
        
        self.editable_group = EditableValueGroup("Firefly")

        self.mesh = MeshObject("Firefly/firefly.obj")
        self.mesh.set_scale_single(50)
        self.add_child(self.mesh)

        material = self.mesh.mesh.material_library.get_or_default("lit_part")
        material.lit_mode = LitMode.UNLIT
        material.color_multiplier_editable = EditableValue(3.0, 0.35, 5, 'Cor')
        self.editable_group.add_editable(material.color_multiplier_editable)

        self.light = LightObject(LightData("Light", [0.8, 0.7, 0], default_intensity=1, max_intensity=1.5))
        self.light.set_pos(np.array([0, 1, -3], dtype=np.float32))
        self.add_child(self.light)
        self.editable_group.add_editable(self.light.light_data.intensity)

        self.fly_center = np.zeros(3)
        self.fly_radius = 0
        self.fly_frequency = 0
        self.is_flying = False
        self.hover_amplitude = 0
        self.hover_frequency = 0
        self.is_hovering = False

    def fly_around(self, center: np.ndarray, radius: float, frequency: float) -> None:
        self.fly_center = center
        self.fly_radius = radius
        self.fly_frequency = frequency
        self.is_flying = True

    def hover(self, amplitude: float = 1.0, frequency: float = 1.0):
        self.is_hovering = True
        self.hover_amplitude = amplitude
        self.hover_frequency = frequency
        self.anchor_y = self.position[1]

    
    def update(self, *args) -> None:
        super().update(*args)

        x, z, rot = self._get_fly_xz_rot()
        y = self._get_hover_y()
        self.set_pos([x, y, z])
        self.set_rot_rad(rot)

    
    def _get_fly_xz_rot(self) -> tuple[float, float]:
        if not self.is_flying:
            return self.position[0], self.position[2], self.rotation
        
        time = glfw.get_time() * self.fly_frequency
        x = np.sin(time) * self.fly_radius + self.fly_center[0]
        z = np.cos(time) * self.fly_radius + self.fly_center[2]
        return x, z, [0, time + np.pi / 2, 0]

    def _get_hover_y(self) -> float:
        if not self.is_hovering:
            return self.position[1]

        anchor_y = self.fly_center[1] if self.is_flying else self.anchor_y
        time = glfw.get_time() * self.hover_frequency
        return np.sin(time) * self.hover_amplitude + anchor_y