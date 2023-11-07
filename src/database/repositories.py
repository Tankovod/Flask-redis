from typing import List, Dict, Any

import orjson as json

from apiflask import HTTPError
from redis import Redis


class RedisRepository:
    def __init__(self, r):
        self.r: Redis = r

    def get(self, prefix: str = None, id_: int = 1, key: str = None) -> Dict | None:
        if not key:
            key = f"{prefix}:{id_}"

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

    def get_all(self, prefix: str) -> List[Dict]:
        keys = self.r.keys(f"{prefix}:*")

        return [self.get(key=key) for key in keys]

    def insert(self, prefix: str, params=None) -> int:
        self.r.incr(f"last_{prefix}_id")
        id_ = self.r.get(f"last_{prefix}_id")

        if self.r.set(name=f"{prefix}:{id_}", nx=True, value=str(params).replace("\'", "\"")) is None:
            raise HTTPError(status_code=400, message="Integrity error", detail="Task is already exists")

        return id_

    def put(self, prefix: str, task_id: int, params=None) -> str:

        if self.r.set(name=f"{prefix}:{task_id}", xx=True, value=str(params).replace("\'", "\"")) is None:
            raise HTTPError(status_code=404, message="Not found", detail="Task was not found")

        return str(task_id)
