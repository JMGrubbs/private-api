from openai_client import openai_client_connection
import time


async def get_messages_openai(thread_id):
    async with openai_client_connection() as client:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        message_list = []
        for message in messages.model_dump().get("data", []):
            message_list.append(
                {
                    "sender": message.get("role"),
                    "text": message.get("content")[0].get("text").get("value"),
                }
            )
        return message_list


async def create_message_openai(thread_id, content, role):
    async with openai_client_connection() as client:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            content=content,
            role=role,
        )
        return message.model_dump()


async def create_run_openai(thread_id, agent_id):
    async with openai_client_connection() as client:
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=agent_id)
        return run.model_dump()


async def get_run_openai(thread_id, run_id):
    async with openai_client_connection() as client:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run.model_dump()


async def get_completion_openai(thread_id, text, sender, agent_id):
    await create_message_openai(thread_id, text, sender)
    run = await create_run_openai(thread_id, agent_id)
    while run.get("status") == "queued" or run.get("status") == "in_progress":
        run = await get_run_openai(thread_id, run.get("id"))
        print(run.get("status"))
        time.sleep(0.5)
    return True
