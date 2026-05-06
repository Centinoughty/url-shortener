import os
import redis
from typing import cast

class RedisManager:
  def __init__(self, redis_url: str | None = None):
    """
    Initialize redis connection

    Args:
      redis_url (str | None):
        Full redis connection URL.
        Falls back to REDIS_URLnv variable.
    """
    
    self.redis_url = (
      redis_url
      if redis_url is not None
      else os.getenv("REDIS_URL", "redis://redis:6379/0")
    )

    self.client = redis.Redis.from_url(
      self.redis_url,
      decode_responses=True
    )


  def get(self, key: str) -> str | None:
    """
    Get value from redis
    """
    
    value = self.client.get(key)
    return value if isinstance(value, str) else None


  def set(self, key: str, value: str, expiry: int = 86400) -> bool:
    """
    Set value in redis with expiry

    Args:
      key: redis key
      value: value to store
      expiry: expiry in seconds (default: 24 hours)
    """
    
    result = self.client.set(key, value, expiry)
    return bool(result)


  def increment(self, key: str) -> int:
    """
    Increment integer value
    """

    result = self.client.incr(key)
    return int(cast(int, result))


  def delete(self, key: str) -> int:
    """
    Delete key from redis store
    """

    result = self.client.delete(key)
    return int(cast(int, result))


  def exists(self, key: str) -> bool:
    """
    Check if key exists
    """
    
    return bool(self.client.exists(key))


  def ping(self) -> bool:
    """
    Check redis connection
    """

    return bool(self.client.ping())
