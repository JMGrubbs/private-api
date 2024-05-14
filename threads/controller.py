from threads.tools import get_threads_db


async def get_proxy_threads(db, proxy_agent_id=None, refresh=False):
    if proxy_agent_id:
        threads = await get_threads_db(db)
    return threads
