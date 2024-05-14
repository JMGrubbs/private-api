from openai_client import openai_client_connection
from cache.tools import get_set_cache_list

from sqlalchemy.sql import text


async def get_agents_openai():
    try:
        agents = []
        async with openai_client_connection() as client:
            agents = client.beta.assistants.list()
            agents = [agent.model_dump() for agent in agents]
        return agents
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


async def create_new_agent_openai(new_agent_package):
    try:
        async with openai_client_connection() as client:
            new_agent = client.beta.assistants.create(
                instructions=new_agent_package.get("instructions", "Please provide instructions"),
                name=new_agent_package.get("name", "New Agent"),
                tools=new_agent_package.get("tools", []),
                model=new_agent_package.get("model", "gpt-3.5-turbo"),
            )
            return new_agent
    except Exception as e:
        print(f"Error creating new agent: {e}")
        return False


async def delete_agent_openai(agent_id):
    try:
        async with openai_client_connection() as client:
            client.beta.assistants.delete(assistant_id=agent_id)
            return True
    except Exception as e:
        print(f"Error deleting agent from OpenAI: {e}")
        return False


async def delete_agent_from_db(agent_id, db):
    try:
        async with db as session:
            sql = text("DELETE FROM chatbot.agents WHERE agent_id = :agent_id;")
            await session.execute(sql, params={"agent_id": agent_id})
            await session.commit()
            return True
    except Exception as e:
        print(f"Error deleting agent from DB: {e}")
        return False


async def insert_update_new_agent_to_db(new_agent, db):
    try:
        async with db as session:
            sql = text(
                """INSERT INTO chatbot.agents (agent_id, name, description, instructions, model, response_format)
                VALUES (:id, :name, :description, :instructions, :model, :response_format)
                RETURNING *;
                """
            )
            await session.execute(sql, params=new_agent["response"])
            await session.commit()
            return True
    except Exception as e:
        print(f"Error inserting new agent to DB: {e}")
        return False


async def select_agents_from_db(db):
    async with db as session:
        stmt = text("SELECT agent_id, name, instructions, description, model FROM chatbot.agents;")
        result = await session.execute(stmt)
        agents = result.fetchall()
        agent_dicts = []
        for agent in agents:
            agent_dict = {
                "agent_id": agent[0],
                "name": agent[1],
                "instructions": agent[2],
                "description": agent[3],
                "model": agent[4],
            }
            agent_dicts.append(agent_dict)
        return agent_dicts


# async def add_agent_to_db(db, agent):
#     async with db as session:
#         sql = text(
#             "INSERT INTO chatbot.agents (agent_id, name, role, instructions) VALUES (:agent_id, :name, :role, :instructions);"
#         )

#         await session.execute(sql, params=agent)


# async def get_threads_db(db):
#     async with db as session:
#         stmt = text("SELECT id, thread_id FROM chatbot.threads;")
#         result = await session.execute(stmt)
#         threads = result.fetchall()
#         threads = [{"id": id, "thread_id": thread_id} for id, thread_id in threads]
#         await get_set_cache(namespace="proxy_threads", obj_type=threads)
#         return threads


# async def create_agent_obj(agent_id):
#     agent_json = await get_agent_from_cache(agent_id)
#     new_agent_obj = Agent(**agent_json)
#     return new_agent_obj
