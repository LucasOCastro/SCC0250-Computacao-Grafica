import numpy as np

class LightData:
    """
    Classe que representa uma fonte de luz em uma cena.
    Possui um cor atual que pode ser modificada com base em intensidade.
    """
    
    def __init__(self,
                 color: np.ndarray,
                 default_intensity: float = 1.0,
                 min_intensity: float = 0.0,
                 max_intensity: float = 1.3,
                 world_position: np.ndarray = [0, 0, 0]):
        self.default_color = np.array(color, dtype=np.float32)
        self.default_intensity = default_intensity
        self._intensity = default_intensity
        self.min_intensity = min_intensity
        self.max_intensity = max_intensity
        self.world_position = np.array(world_position, dtype=np.float32)
    
    @property
    def color(self):
        return self.default_color * self._intensity
    
    @property
    def intensity(self):
        return self._intensity
    
    @intensity.setter
    def intensity(self, value):
        self._intensity = max(min(value, self.max_intensity), self.min_intensity)
    
    def reset(self):
        self._intensity = self.default_intensity
    