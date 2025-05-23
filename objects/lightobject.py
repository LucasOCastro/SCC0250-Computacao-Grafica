from objects.object import Object
from rendering.lightdata import LightData

class LightObject(Object):
    def __init__(self, light_data: LightData):
        super().__init__()
        self.light_data = light_data