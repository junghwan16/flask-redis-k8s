import pytest
from unittest.mock import Mock
from src.presentation.app import create_app
from src.domain.counter import Counter
from src.domain.repositories import CounterRepository


class FakeCounterRepository(CounterRepository):
    def __init__(self):
        self.counters = {}
    
    def save(self, counter: Counter) -> None:
        self.counters[counter.name] = counter
    
    def find_by_name(self, name: str):
        return self.counters.get(name)
    
    def find_all(self):
        return self.counters.copy()
    
    def delete(self, name: str) -> bool:
        if name in self.counters:
            del self.counters[name]
            return True
        return False


@pytest.fixture
def app():
    repository = FakeCounterRepository()
    app = create_app(repository)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestCounterAPI:
    def test_get_counter_returns_zero_for_new(self, client):
        response = client.get("/api/v1/counters/new_counter")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "new_counter"
        assert data["value"] == 0
    
    def test_increment_counter(self, client):
        response = client.post("/api/v1/counters/test/increment", json={})
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "test"
        assert data["value"] == 1
        
        response = client.post("/api/v1/counters/test/increment", json={"amount": 5})
        assert response.status_code == 200
        data = response.get_json()
        assert data["value"] == 6
    
    def test_reset_counter(self, client):
        client.post("/api/v1/counters/test/increment", json={"amount": 10})
        
        response = client.post("/api/v1/counters/test/reset")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "test"
        assert data["value"] == 0
    
    def test_get_all_counters(self, client):
        client.post("/api/v1/counters/counter1/increment", json={})
        client.post("/api/v1/counters/counter2/increment", json={"amount": 5})
        
        response = client.get("/api/v1/counters")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["counters"]) == 2
        assert data["counters"]["counter1"]["value"] == 1
        assert data["counters"]["counter2"]["value"] == 5
    
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
    
    def test_invalid_increment_amount(self, client):
        response = client.post("/api/v1/counters/test/increment", json={"amount": -1})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data