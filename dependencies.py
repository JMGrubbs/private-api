import asyncio
import json
from cache.cache import redis_connection
from fastapi import HTTPException, Header
from database import async_session_factory
import os
from sessions.data_classes import UserSession

API_KEY = os.getenv("API_KEY")
DEFAULT_EXPERATION = 60 * 60 * 12


async def create_user_sessions(user_session: UserSession):
    print(user_session)
    try:
        async with redis_connection() as rd:
            session_key = f"user_session:{user_session.session_id}"
            await rd.setex(session_key, DEFAULT_EXPERATION, user_session.model_dump_json())
            return True
    except Exception as e:
        print("User session not added to cach", e)


async def check_user_session(user_session_id):
    try:
        async with redis_connection() as rd:
            session_key = f"user_session:{user_session_id}"
            session = await rd.get(session_key)
            print(session)
            if not session:
                return False
            return True
    except Exception as e:
        print("error getting session", e)


async def get_set_cache_list(*args, **kwargs):
    namespace = kwargs.get("namespace")
    elements = kwargs.get("elements")
    callback = kwargs.get("cb")
    try:
        async with redis_connection() as rd:
            if elements:
                await rd.delete(namespace)
                for el in elements:
                    await rd.rpush(namespace, json.dumps(el))
                return True
            else:
                elements = await rd.lrange(namespace, 0, -1)
                if elements:
                    return [json.loads(el) for el in elements]
                else:
                    elements = await callback(db=kwargs.get("db"))
                    await rd.delete(namespace)
                    for el in elements:
                        await rd.rpush(namespace, json.dumps(el))
                    return elements
    except Exception as e:
        print("Error in get_set_cache_list:", e)


async def remove_from_cache_list(agent_id, namespace):
    try:
        async with redis_connection() as rd:
            list_length = await rd.llen(namespace)
            all_items = await rd.lrange(namespace, 0, list_length - 1)

            for item in all_items:
                obj = json.loads(item)
                if obj.get("agent_id") == agent_id:
                    await rd.lrem(namespace, 0, item)
                    return True
    except Exception as e:
        print(f"Error removing agent from cache: {e}")
        return False


async def empty_namespace(namespace):
    try:
        async with redis_connection() as rd:
            await rd.delete(namespace)
            return True
    except Exception as e:
        print(f"Error removing agent from cache: {e}")
        return False


def validate_api_key(api_key: str = Header(...), user_session_id: str = Header(...)):
    current_session = check_user_session(user_session_id=user_session_id)
    if api_key != API_KEY and current_session:
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
