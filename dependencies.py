import asyncio
from fastapi import HTTPException, Header
from database import async_session_factory
import os

API_KEY = os.getenv("API_KEY")


def validate_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return True


tasks_queue = asyncio.Queue()
is_worker_active = False


async def worker():
    global is_worker_active
    is_worker_active = True
    try:
        while True:
            task_func, args, kwargs = await tasks_queue.get()
            try:
                await task_func(*args, **kwargs)
            except Exception as e:
                print(f"Error executing task: {e}")
            tasks_queue.task_done()
    finally:
        is_worker_active = False


async def db_session():
    async with async_session_factory() as session:
        yield session
