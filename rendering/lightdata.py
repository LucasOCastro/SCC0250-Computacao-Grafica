import numpy as np
from editablevalue import EditableValue;

class LightData:
    """
    Classe que representa uma fonte de luz em uma cena.
    Possui um cor atual que pode ser modificada com base em intensidade.
    """
    
    def __init__(self,
                 name: str,
                 color: np.ndarray,
                 default_intensity: float = 1.0,
                 min_intensity: float = 0.0,
                 max_intensity: float = 1.5,
                 world_position: np.ndarray = [0, 0, 0]):
        self.name = name
        self.default_color = np.array(color, dtype=np.float32)
        self.intensity = EditableValue(default_intensity, min_intensity, max_intensity, name + ' Intensity')
        self.world_position = np.array(world_position, dtype=np.float32)
    
    @property
    def color(self) -> np.ndarray:
        return self.default_color * self.intensity.value
    
    def reset(self):
        self.intensity = self.default_intensity
    