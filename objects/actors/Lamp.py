from objects.object import Object
from objects.meshobject import MeshObject
from objects.lightobject import LightObject
from rendering.lightdata import LightData
from rendering.litmode  import LitMode
from editablevalue import EditableValueGroup, EditableValue


class Lamp(Object):
    def __init__(self):
        super().__init__()
        
        self.editable_group = EditableValueGroup("Lâmpada")

        self.mesh = MeshObject("lamp/HangingLamp.obj")
        self.mesh.set_scale_single(0.01)
        self.add_child(self.mesh)

        material = self.mesh.mesh.material_library.get_or_default("lit_part")
        material.lit_mode = LitMode.UNLIT
        material.color_multiplier_editable = EditableValue(3.0, 0.35, 5, 'Cor')
        self.editable_group.add_editable(material.color_multiplier_editable)

        #duas luzes com mesmo editavel para garantir q a lampada seja iluminada
        self.light_front = self._make_light(-1)
        self.add_child(self.light_front)
        self.editable_group.add_editable(self.light_front.light_data.intensity)

        self.light_back = self._make_light(1)
        self.add_child(self.light_back)
        self.editable_group.add_editable(self.light_back.light_data.intensity)

        self.light_data = [self.light_front.light_data, self.light_back.light_data]


    def _make_light(self, side_multiplier: int) -> LightObject:
        light = LightObject(LightData(f"Luz {side_multiplier}", [0, 0.8, 0.5], default_intensity=0.5, max_intensity=.75))
        light.set_pos([0, -23, side_multiplier])
        test_mesh = MeshObject("particles/skull1/Skull.obj", lit_mode=LitMode.UNLIT)
        test_mesh.set_scale_single(2)
        light.add_child(test_mesh)
        return light
    
    