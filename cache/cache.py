from redis.asyncio import Redis
from contextlib import asynccontextmanager
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")


@asynccontextmanager
async def redis_connection():
    client = await Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()
