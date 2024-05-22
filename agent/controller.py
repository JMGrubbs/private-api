from cache.tools import get_set_cache_list, remove_from_cache_list
from agent.tools import (
    get_agents_openai,
    create_new_agent_openai,
    delete_agent_from_db,
    delete_agent_openai,
    select_agents_from_db,
    insert_update_new_agent_to_db,
)


async def retrieve_agents(db):
    agents = await get_agents_openai()
    for agent in agents:
        await insert_update_new_agent_to_db({"response": agent}, db)
    return True


async def create_agents(new_agent_package, db):
    new_agent = await create_new_agent_openai(new_agent_package)
    if new_agent:
        sql_status = await insert_update_new_agent_to_db(new_agent, db)
        if sql_status:
            return new_agent
    return False


async def select_agents(db):
    agents = await get_set_cache_list(namespace="agents", cb=select_agents_from_db, db=db)
    return agents


async def delete_agent(agent_id, db):
    result = await delete_agent_from_db(agent_id, db)
    if result:
        result = await delete_agent_openai(agent_id)
    if result:
        result = await remove_from_cache_list(agent_id, namespace="agents")
    return result
