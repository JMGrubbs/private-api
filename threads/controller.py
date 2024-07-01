from threads.tools import get_threads_db, create_thread_openai, insert_thread_db, delete_thread_db


async def select_threads(db):
    threads = await get_threads_db(db)
    return threads


async def create_thread(db):
    new_thread = await create_thread_openai()
    new_thread = await insert_thread_db(new_thread, db)
    return new_thread


async def delete_thread(db, thread_id):
    result = await delete_thread_db(thread_id, db)
    return result
