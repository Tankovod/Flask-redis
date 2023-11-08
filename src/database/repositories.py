from typing import List, Dict
from src.settings import redis
import orjson as json
from abc import ABC, abstractmethod
from apiflask import HTTPError
from redis import Redis


class AbstractRepository(ABC):

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def insert(self):
        raise NotImplementedError

    @abstractmethod
    def put(self):
        raise NotImplementedError


class RedisRepository(AbstractRepository):

    def __init__(self, r, prefix):
        self.r: Redis = r
        self.prefix = prefix

    def get(self, id_: int = 1, key: str = None) -> Dict | None:
        if not key:
            key = f"{self.prefix}:{id_}"

        type_check = self.r.type(key)
        if type_check == "string":
            value = self.r.get(key)
        elif type_check == "hash":
            value = self.r.hgetall(key)
        elif type_check == "zset":
            value = self.r.zrange(key, 0, -1)
        elif type_check == "list":
            value = self.r.lrange(key, 0, -1)
        elif type_check == "set":
            value = self.r.smembers(key)
        else:
            return None

        return {key: json.loads(value)}

    def get_all(self) -> List[Dict]:
        keys = self.r.keys(f"{self.prefix}:*")

        return [self.get(key=key) for key in keys]

    def insert(self, params=None) -> int:
        self.r.incr(f"last_{self.prefix}_id")
        id_ = self.r.get(f"last_{self.prefix}_id")

        if self.r.set(name=f"{self.prefix}:{id_}", nx=True, value=str(params).replace("\'", "\"")) is None:
            raise HTTPError(status_code=400, message="Integrity error", detail="Task is already exists")

        return id_

    def put(self, task_id: int, params=None) -> str:

        if self.r.set(name=f"{self.prefix}:{task_id}", xx=True, value=str(params).replace("\'", "\"")) is None:
            raise HTTPError(status_code=404, message="Not found", detail="Task was not found")

        return str(task_id)


class TaskRepository(RedisRepository):

    def __init__(self, r=redis, prefix="task"):
        super().__init__(r, prefix)
