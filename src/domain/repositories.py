from abc import ABC, abstractmethod
from typing import Optional, Dict
from src.domain.counter import Counter


class CounterRepository(ABC):
    @abstractmethod
    def save(self, counter: Counter) -> None:
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Counter]:
        pass
    
    @abstractmethod
    def find_all(self) -> Dict[str, Counter]:
        pass
    
    @abstractmethod
    def delete(self, name: str) -> bool:
        pass