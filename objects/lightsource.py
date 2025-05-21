from objects.object import Object
import numpy as np

class LightSource(Object):
    def __init__(self, color: np.ndarray = np.array([1.0, 1.0, 1.0], dtype=np.float32)):
        super().__init__()
        self.color = color