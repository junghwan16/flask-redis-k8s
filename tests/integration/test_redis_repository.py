import pytest
from fakeredis import FakeRedis
from src.infrastructure.repositories import RedisCounterRepository
from src.domain.counter import Counter


class TestRedisCounterRepository:
    @pytest.fixture
    def redis_client(self):
        return FakeRedis(decode_responses=True)
    
    @pytest.fixture
    def repository(self, redis_client):
        return RedisCounterRepository(redis_client)
    
    def test_save_and_find_counter(self, repository):
        counter = Counter("page_views", initial_value=42)
        
        repository.save(counter)
        
        found = repository.find_by_name("page_views")
        assert found is not None
        assert found.name == "page_views"
        assert found.value == 42
    
    def test_find_nonexistent_counter(self, repository):
        found = repository.find_by_name("nonexistent")
        assert found is None
    
    def test_find_all_counters(self, repository):
        counter1 = Counter("api_calls", 100)
        counter2 = Counter("errors", 5)
        counter3 = Counter("logins", 250)
        
        repository.save(counter1)
        repository.save(counter2)
        repository.save(counter3)
        
        all_counters = repository.find_all()
        
        assert len(all_counters) == 3
        assert "api_calls" in all_counters
        assert "errors" in all_counters
        assert "logins" in all_counters
        assert all_counters["api_calls"].value == 100
        assert all_counters["errors"].value == 5
        assert all_counters["logins"].value == 250
    
    def test_delete_counter(self, repository):
        counter = Counter("temp_counter", 10)
        repository.save(counter)
        
        deleted = repository.delete("temp_counter")
        assert deleted is True
        
        found = repository.find_by_name("temp_counter")
        assert found is None
    
    def test_delete_nonexistent_counter(self, repository):
        deleted = repository.delete("nonexistent")
        assert deleted is False
    
    def test_counter_persistence_after_modification(self, repository):
        counter = Counter("sessions", 10)
        repository.save(counter)
        
        found = repository.find_by_name("sessions")
        found.increment(5)
        repository.save(found)
        
        updated = repository.find_by_name("sessions")
        assert updated.value == 15