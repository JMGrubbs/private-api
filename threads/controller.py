from cache.tools import get_set_cache
from threads.tools import get_threads_db


async def get_proxy_threads(db, proxy_agent_id=None, refresh=False):
    threads = await get_set_cache(namespace="proxy_threads")
    print("threads", threads)
    if proxy_agent_id:
        threads = await get_threads_db(db)

    return threads
