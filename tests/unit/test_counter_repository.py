import pytest
from abc import ABC, abstractmethod
from typing import Optional, Dict
from src.domain.counter import Counter
from src.domain.repositories import CounterRepository


class TestCounterRepository:
    def test_repository_is_abstract(self):
        with pytest.raises(TypeError):
            CounterRepository()
    
    def test_repository_defines_interface(self):
        assert hasattr(CounterRepository, 'save')
        assert hasattr(CounterRepository, 'find_by_name')
        assert hasattr(CounterRepository, 'find_all')
        assert hasattr(CounterRepository, 'delete')


class FakeCounterRepository(CounterRepository):
    def __init__(self):
        self._counters: Dict[str, Counter] = {}
    
    def save(self, counter: Counter) -> None:
        self._counters[counter.name] = counter
    
    def find_by_name(self, name: str) -> Optional[Counter]:
        return self._counters.get(name)
    
    def find_all(self) -> Dict[str, Counter]:
        return self._counters.copy()
    
    def delete(self, name: str) -> bool:
        if name in self._counters:
            del self._counters[name]
            return True
        return False


class TestFakeCounterRepository:
    def test_save_and_find_counter(self):
        repo = FakeCounterRepository()
        counter = Counter("visits", initial_value=10)
        
        repo.save(counter)
        
        found = repo.find_by_name("visits")
        assert found is not None
        assert found.name == "visits"
        assert found.value == 10
    
    def test_find_nonexistent_counter(self):
        repo = FakeCounterRepository()
        
        found = repo.find_by_name("nonexistent")
        assert found is None
    
    def test_find_all_counters(self):
        repo = FakeCounterRepository()
        counter1 = Counter("counter1", 5)
        counter2 = Counter("counter2", 10)
        
        repo.save(counter1)
        repo.save(counter2)
        
        all_counters = repo.find_all()
        assert len(all_counters) == 2
        assert "counter1" in all_counters
        assert "counter2" in all_counters
    
    def test_delete_counter(self):
        repo = FakeCounterRepository()
        counter = Counter("temp")
        
        repo.save(counter)
        assert repo.find_by_name("temp") is not None
        
        deleted = repo.delete("temp")
        assert deleted is True
        assert repo.find_by_name("temp") is None
    
    def test_delete_nonexistent_counter(self):
        repo = FakeCounterRepository()
        
        deleted = repo.delete("nonexistent")
        assert deleted is False