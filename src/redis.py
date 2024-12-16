import redis.asyncio as redis
from fastapi import FastAPI

redis_client = None


async def get_redis():
    return redis_client


async def init_redis(app: FastAPI):
    global redis_client
    redis_client = redis.from_url(app.state.redis_url)


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
