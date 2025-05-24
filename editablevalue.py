class EditableValue:
    """Define um valor editável para mapeamento de input."""
    def __init__(self, default_value: float, min_value: float, max_value: float, label: str):
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self._value = default_value
        self.label = label

    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = max(min(value, self.max_value), self.min_value)
    
    def reset(self):
        self._value = self.default_value