from typing import Dict
from src.domain.counter import Counter
from src.domain.repositories import CounterRepository


class IncrementCounterUseCase:
    def __init__(self, repository: CounterRepository):
        self.repository = repository
    
    def execute(self, name: str, amount: int = 1) -> int:
        counter = self.repository.find_by_name(name)
        
        if counter is None:
            counter = Counter(name)
        
        new_value = counter.increment(amount)
        self.repository.save(counter)
        
        return new_value


class GetCounterUseCase:
    def __init__(self, repository: CounterRepository):
        self.repository = repository
    
    def execute(self, name: str) -> Counter:
        counter = self.repository.find_by_name(name)
        
        if counter is None:
            counter = Counter(name)
        
        return counter


class ResetCounterUseCase:
    def __init__(self, repository: CounterRepository):
        self.repository = repository
    
    def execute(self, name: str) -> None:
        counter = self.repository.find_by_name(name)
        
        if counter is None:
            counter = Counter(name)
        else:
            counter.reset()
        
        self.repository.save(counter)


class GetAllCountersUseCase:
    def __init__(self, repository: CounterRepository):
        self.repository = repository
    
    def execute(self) -> Dict[str, Counter]:
        return self.repository.find_all()