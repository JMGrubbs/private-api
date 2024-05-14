import json

from cache.cache import redis_connection


async def get_set_cache_list(*args, **kwargs):
    namespace = kwargs.get("namespace")
    elements = kwargs.get("elements")
    callback = kwargs.get("cb")
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
