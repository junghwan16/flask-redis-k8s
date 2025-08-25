import pytest
from src.domain.counter import Counter
from src.domain.exceptions import InvalidCounterOperationError


class TestCounter:
    def test_create_counter_with_name(self):
        counter = Counter("page_views")
        assert counter.name == "page_views"
        assert counter.value == 0
    
    def test_create_counter_with_initial_value(self):
        counter = Counter("downloads", initial_value=100)
        assert counter.name == "downloads"
        assert counter.value == 100
    
    def test_increment_counter_by_one(self):
        counter = Counter("clicks")
        new_value = counter.increment()
        assert new_value == 1
        assert counter.value == 1
    
    def test_increment_counter_by_amount(self):
        counter = Counter("score")
        new_value = counter.increment(5)
        assert new_value == 5
        assert counter.value == 5
        
        new_value = counter.increment(3)
        assert new_value == 8
        assert counter.value == 8
    
    def test_cannot_increment_by_negative_amount(self):
        counter = Counter("points")
        with pytest.raises(InvalidCounterOperationError):
            counter.increment(-1)
    
    def test_reset_counter(self):
        counter = Counter("attempts", initial_value=10)
        counter.increment(5)
        assert counter.value == 15
        
        counter.reset()
        assert counter.value == 0
    
    def test_counter_equality(self):
        counter1 = Counter("test", initial_value=5)
        counter2 = Counter("test", initial_value=5)
        counter3 = Counter("other", initial_value=5)
        
        assert counter1 == counter2
        assert counter1 != counter3
    
    def test_counter_string_representation(self):
        counter = Counter("api_calls", initial_value=42)
        assert str(counter) == "Counter(name='api_calls', value=42)"