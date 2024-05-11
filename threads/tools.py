from openai_client import openai_client_connection
from cache.tools import get_set_cache
from sqlalchemy.sql import text


async def create_thread():
    async with openai_client_connection() as client:
        new_thread = client.beta.threads.create()
        await get_set_cache(
            key=new_thread.id,
            namespace="threads",
            obj_type=new_thread.model_dump(),
        )
        return new_thread


async def get_thread_from_openai(thread_id):
    async with openai_client_connection() as client:
        return client.beta.threads.retrieve(thread_id).model_dump()


# async def get_thread(thread_id):
#     return await get_set_cache(key=thread_id, namespace="threads")


# async def get_threads():
#     return await get_set_cache(key=None, namespace="threads")


# async def create_new_message(thread_id, message):
#     async with openai_client_connection() as client:
#         new_message = client.beta.threads.messages.create(
#             thread_id=thread_id, text=message, role="user"
#         )
#         return new_message.model_dump()


async def get_threads_db(db):
    async with db as session:
        stmt = text("SELECT id, thread_id FROM chatbot.threads;")
        result = await session.execute(stmt)
        threads = result.fetchall()
        threads = [{"id": id, "thread_id": thread_id} for id, thread_id in threads]
        ret = await get_set_cache(namespace="proxy_threads", obj_type=threads)
        print("ret", ret)
