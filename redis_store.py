import json
import os
from typing import Optional

import redis


class RedisStore:
    def __init__(self):
        self.url = os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0"
        )

        self.client = redis.from_url(
            self.url,
            decode_responses=True
        )

    def set(
        self,
        key: str,
        value,
        expires: Optional[int] = None
    ):
        payload = json.dumps(
            value,
            ensure_ascii=False
        )

        if expires:
            return self.client.setex(
                key,
                expires,
                payload
            )

        return self.client.set(
            key,
            payload
        )

    def get(self, key: str):
        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def delete(self, key: str):
        return self.client.delete(key)

    def exists(self, key: str):
        return bool(
            self.client.exists(key)
        )


redis_store = RedisStore()
