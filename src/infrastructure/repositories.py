from typing import Optional, Dict
import json
import redis
from src.domain.counter import Counter
from src.domain.repositories import CounterRepository


class RedisCounterRepository(CounterRepository):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.prefix = "counter:"
    
    def save(self, counter: Counter) -> None:
        key = f"{self.prefix}{counter.name}"
        value = {
            "name": counter.name,
            "value": counter.value
        }
        self.redis.set(key, json.dumps(value))
    
    def find_by_name(self, name: str) -> Optional[Counter]:
        key = f"{self.prefix}{name}"
        data = self.redis.get(key)
        
        if data is None:
            return None
        
        counter_data = json.loads(data)
        return Counter(
            name=counter_data["name"],
            initial_value=counter_data["value"]
        )
    
    def find_all(self) -> Dict[str, Counter]:
        pattern = f"{self.prefix}*"
        keys = self.redis.keys(pattern)
        
        counters = {}
        for key in keys:
            counter_name = key.replace(self.prefix, "")
            counter = self.find_by_name(counter_name)
            if counter:
                counters[counter_name] = counter
        
        return counters
    
    def delete(self, name: str) -> bool:
        key = f"{self.prefix}{name}"
        result = self.redis.delete(key)
        return bool(result)