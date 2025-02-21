import redis
from config import REDIS_URL

redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL,
    max_connections=100,
    decode_responses=True
)

redis_client = redis.Redis(connection_pool=redis_pool)

def cache_response(user_message: str, response: str, ttl=300):
    redis_client.setex(user_message, ttl, response)

def get_cached_response(user_message: str):
    return redis_client.get(user_message)