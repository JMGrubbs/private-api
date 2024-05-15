from messages.tools import get_messages_openai, get_completion_openai
from threads.tools import get_openai_thread_id


async def get_messages(id, db):
    thread_id = await get_openai_thread_id(id, db)
    messages = await get_messages_openai(thread_id)
    return messages


async def send_message(request_body, db):
    text = request_body.get("text", None)
    sender = request_body.get("sender", None)
    thread_id = request_body.get("thread", None)
    agent_id = request_body.get("proxy", None)
    if thread_id:
        thread_id = await get_openai_thread_id(thread_id, db)
    if not text or not sender:
        return False
    if not thread_id:
        # new_thread = await get_openai_thread_id(sender, db)
        pass
    new_message = await get_completion_openai(thread_id, text, sender, agent_id)
    return new_message
