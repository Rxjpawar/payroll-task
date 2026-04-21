import json
from src.core.redis_client import redis_client

CACHE_TTL = 300  #(5 minutes paryant cache rahil)


def generate_cache_key(user_id: str, query: str) -> str:
    return f"rag:{user_id}:{query.lower().strip()}"


def get_cached_response(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cached_response(key: str, value: dict):
    redis_client.setex(key, CACHE_TTL, json.dumps(value))


def invalidate_user_cache(user_id: str):
    pattern = f"rag:{user_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)