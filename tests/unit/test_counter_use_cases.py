import pytest
from unittest.mock import Mock
from src.application.use_cases import (
    IncrementCounterUseCase,
    GetCounterUseCase,
    ResetCounterUseCase,
    GetAllCountersUseCase
)
from src.domain.counter import Counter
from src.domain.repositories import CounterRepository


class TestIncrementCounterUseCase:
    def test_increment_existing_counter(self):
        mock_repo = Mock(spec=CounterRepository)
        existing_counter = Counter("views", initial_value=5)
        mock_repo.find_by_name.return_value = existing_counter
        
        use_case = IncrementCounterUseCase(mock_repo)
        result = use_case.execute("views", amount=3)
        
        assert result == 8
        mock_repo.save.assert_called_once_with(existing_counter)
    
    def test_increment_new_counter(self):
        mock_repo = Mock(spec=CounterRepository)
        mock_repo.find_by_name.return_value = None
        
        use_case = IncrementCounterUseCase(mock_repo)
        result = use_case.execute("new_counter", amount=1)
        
        assert result == 1
        mock_repo.save.assert_called_once()
        saved_counter = mock_repo.save.call_args[0][0]
        assert saved_counter.name == "new_counter"
        assert saved_counter.value == 1


class TestGetCounterUseCase:
    def test_get_existing_counter(self):
        mock_repo = Mock(spec=CounterRepository)
        counter = Counter("downloads", initial_value=100)
        mock_repo.find_by_name.return_value = counter
        
        use_case = GetCounterUseCase(mock_repo)
        result = use_case.execute("downloads")
        
        assert result.name == "downloads"
        assert result.value == 100
    
    def test_get_nonexistent_counter_returns_zero(self):
        mock_repo = Mock(spec=CounterRepository)
        mock_repo.find_by_name.return_value = None
        
        use_case = GetCounterUseCase(mock_repo)
        result = use_case.execute("nonexistent")
        
        assert result.name == "nonexistent"
        assert result.value == 0


class TestResetCounterUseCase:
    def test_reset_existing_counter(self):
        mock_repo = Mock(spec=CounterRepository)
        counter = Counter("attempts", initial_value=10)
        mock_repo.find_by_name.return_value = counter
        
        use_case = ResetCounterUseCase(mock_repo)
        use_case.execute("attempts")
        
        assert counter.value == 0
        mock_repo.save.assert_called_once_with(counter)
    
    def test_reset_nonexistent_counter_creates_new(self):
        mock_repo = Mock(spec=CounterRepository)
        mock_repo.find_by_name.return_value = None
        
        use_case = ResetCounterUseCase(mock_repo)
        use_case.execute("new_counter")
        
        mock_repo.save.assert_called_once()
        saved_counter = mock_repo.save.call_args[0][0]
        assert saved_counter.name == "new_counter"
        assert saved_counter.value == 0


class TestGetAllCountersUseCase:
    def test_get_all_counters(self):
        mock_repo = Mock(spec=CounterRepository)
        counters = {
            "counter1": Counter("counter1", 10),
            "counter2": Counter("counter2", 20)
        }
        mock_repo.find_all.return_value = counters
        
        use_case = GetAllCountersUseCase(mock_repo)
        result = use_case.execute()
        
        assert len(result) == 2
        assert "counter1" in result
        assert "counter2" in result
        assert result["counter1"].value == 10
        assert result["counter2"].value == 20