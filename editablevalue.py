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
    
    def apply_delta(self, delta: float):
        self.value += delta

    def reset(self):
        self.value = self.default_value

    def __str__(self):
        return f"{self.label}: {self.value:.2f}"

class EditableValueGroup(EditableValue):
    """
    Grupo de valores editáveis, controlando um conjunto de floats.
    Valor de 0 a 2, normaliza o valor de cada editável entre min e default ou entre default e max.
    """
    def __init__(self, label: str, editables: list[EditableValue] = []):
        super().__init__(1, 0, 2, label)

        self.editables: dict[str, EditableValue] = {}
        for editable in editables:
            self.add_editable(editable)

    def add_editable(self, editable: EditableValue):
        self.editables[editable.label] = editable

    @EditableValue.value.setter
    def value(self, value: float):
        EditableValue.value.fset(self, value)
        for editable in self.editables.values():
            editable.value = self.normalize(value, editable)
            
    def normalize(self, value: float, editable: EditableValue) -> float:
        def normalize_between(value: float, min_value: float, max_value: float) -> float:
            return value * (max_value - min_value) + min_value
        
        if value <= 1:
            return normalize_between(value, editable.min_value, editable.default_value)
        return normalize_between(value - 1, editable.default_value, editable.max_value)