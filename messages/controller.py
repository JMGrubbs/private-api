from messages.tools import get_messages_openai, get_completion_openai
from threads.controller import create_thread


async def get_messages(thread_id):
    messages = await get_messages_openai(thread_id)
    return messages


async def send_message(request_body, db):
    text = request_body.get("text", None)
    sender = request_body.get("sender", None)
    thread_id = request_body.get("thread", None)
    agent_id = request_body.get("proxy", None)
    if not text or not sender:
        return False
    if not thread_id:
        new_thread = await create_thread(db)
        thread_id = new_thread.get("id")
    run_result = await get_completion_openai(thread_id, text, sender, agent_id)
    if not run_result:
        return False
    all_messages = await get_messages(thread_id)
    return all_messages
