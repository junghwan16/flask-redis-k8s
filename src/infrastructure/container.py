import os
import redis
from src.infrastructure.repositories import RedisCounterRepository
from src.domain.repositories import CounterRepository


class Container:
    def __init__(self):
        self._redis_client = None
        self._repository = None
    
    @property
    def redis_client(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                decode_responses=True
            )
        return self._redis_client
    
    @property
    def counter_repository(self) -> CounterRepository:
        if self._repository is None:
            self._repository = RedisCounterRepository(self.redis_client)
        return self._repository