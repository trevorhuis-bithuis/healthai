import os
import redis

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))
