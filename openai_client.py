from contextlib import asynccontextmanager
import os
from openai import OpenAI

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


@asynccontextmanager
async def openai_client_connection():
    CLIENT = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )
    try:
        yield CLIENT
    finally:
        CLIENT.close()
