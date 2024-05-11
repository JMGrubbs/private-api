from cache.tools import get_set_cache
from agent.tools import get_agent_by_id, get_agents_openai


async def get_agents(agent_id=None):
    if agent_id:
        return await get_agent_by_id(agent_id)

    agents = await get_set_cache(namespace="agents")
    if not agents:
        agents = await get_agents_openai()
        return True

    return list(agents.values())
