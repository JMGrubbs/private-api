from openai_client import openai_client_connection
from sqlalchemy.sql import text
from threads.data_classes import Thread
from typing import List


async def create_thread_openai():
    async with openai_client_connection() as client:
        new_thread = client.beta.threads.create()
        return new_thread.model_dump()


async def get_thread_from_openai(thread_id):
    async with openai_client_connection() as client:
        return client.beta.threads.retrieve(thread_id).model_dump()


# async def create_new_message(thread_id, message):
#     async with openai_client_connection() as client:
#         new_message = client.beta.threads.messages.create(
#             thread_id=thread_id, text=message, role="user"
#         )
#         return new_message.model_dump()


async def get_threads_db(db) -> List[Thread]:
    try:
        async with db as session:
            stmt = text("SELECT id, thread_id, name, status FROM chatbot.threads WHERE status = true;")
            result = await session.execute(stmt)
            threads = result.fetchall()
            threads = [Thread(id=id, thread_id=thread_id, name=name, status=status) for id, thread_id, name, status in threads]
            return threads
    except Exception as e:
        print("Error getting threads from db:", e)
        return False


async def insert_thread_db(new_thread, db) -> Thread | bool:
    try:
        async with db as session:
            stmt = text(
                "INSERT INTO chatbot.threads (thread_id) VALUES (:thread_id) ON CONFLICT (thread_id) DO NOTHING RETURNING id, name, status, thread_id;"
            )
            result = await session.execute(stmt, {"thread_id": new_thread["id"]})
            result = result.fetchone()
            await session.commit()
            new_thread = Thread(id=result[0], name=result[1], status=result[2], thread_id=result[3])
            return new_thread
    except Exception as e:
        print("Error inserting new thread:", e)
        return False


async def get_openai_thread_id(id, db):
    async with db as session:
        stmt = text("SELECT thread_id FROM chatbot.threads WHERE id=:id AND status = true;")
        result = await session.execute(stmt, {"id": id})
        thread_id = result.fetchone()
        return thread_id[0] if thread_id else None


async def delete_thread_db(id, db):
    try:
        async with db as session:
            stmt = text("UPDATE chatbot.threads SET status = False WHERE id = :id;")
            await session.execute(stmt, {"id": id})
            await session.commit()
            return True
    except Exception as e:
        print("Error deleting thread:", e)
        return False
