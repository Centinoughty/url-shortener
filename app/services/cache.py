import redis
import os
from typing import cast

r = redis.Redis(
  host=os.getenv("REDIS_HOST", "redis"),
  port=6379,
  decode_responses=True
)

def get(key) -> str | None:
  return cast(str | None, r.get(key))


def set(key, value) -> None:
  r.set(key, value, ex=86400)


def increment(key) -> int:
  return cast(int, r.incr(key))
