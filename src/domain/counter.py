from src.domain.exceptions import InvalidCounterOperationError


class Counter:
    def __init__(self, name: str, initial_value: int = 0):
        self._name = name
        self._value = initial_value
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> int:
        return self._value
    
    def increment(self, amount: int = 1) -> int:
        if amount < 0:
            raise InvalidCounterOperationError("Cannot increment by negative amount")
        self._value += amount
        return self._value
    
    def reset(self) -> None:
        self._value = 0
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Counter):
            return False
        return self.name == other.name and self.value == other.value
    
    def __str__(self) -> str:
        return f"Counter(name='{self.name}', value={self.value})"