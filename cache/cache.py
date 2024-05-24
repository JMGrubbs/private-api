from redis.asyncio import Redis
from contextlib import asynccontextmanager
import os

REDIS_URL = os.getenv("REDIS_URL")


@asynccontextmanager
async def redis_connection():
    client = await Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()
