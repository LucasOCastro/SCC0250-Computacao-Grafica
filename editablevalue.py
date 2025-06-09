import abc

class BaseEditableValue(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply_delta(self, delta: float):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

class EditableValue(BaseEditableValue):
    """Define um valor editável para mapeamento de input."""
    def __init__(self,
                 default_value: float,
                 min_value: float,
                 max_value: float,
                 label: str,
                 callback: callable = None):
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self._value = default_value
        self.label = label
        self.callback: callable = callback

    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = max(min(value, self.max_value), self.min_value)
        if self.callback is not None:
            self.callback(self._value)
    
    def apply_delta(self, delta: float):
        self.value += delta
    
    def reset(self):
        self._value = self.default_value

    def __str__(self):
        return f"{self.label}: {self.value:.2f}"

class EditableValueGroup:
    def __init__(self, label: str):
        self.label = label
        self.editables: dict[str, EditableValue] = {}

    def add_editable(self, editable: EditableValue):
        self.editables[editable.label] = editable

    def apply_delta(self, delta: float):
        for editable in self.editables.values():
            editable.apply_delta(delta)
    
    def reset(self):
        for editable in self.editables:
            editable.reset()

    def __str__(self):
        editable_strings = [str(editable) for editable in self.editables.values()]
        return f"{self.label}: {', '.join(editable_strings)}"