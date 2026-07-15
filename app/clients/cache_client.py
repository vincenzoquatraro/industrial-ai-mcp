import json
import redis

from app.config import settings

class CacheClient:
    """
    Wrap attorno a Redis, isolo libreria esterna
    """

    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL, decode_responses= True)
    
    def get(self, key:str):
        raw = self.client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    
    def set(self, key:str, value, ttl_seconds:int = 300):
        ttl = ttl_seconds or settings.CACHE_TTL_SECONDS
        self.client.set(key, json.dumps(value), ex=ttl)