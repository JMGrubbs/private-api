from fastapi import APIRouter, HTTPException, Request
import os
from threads.tools import (
    create_thread,
    get_threads,
)

API_KEY = os.getenv("API_KEY")


threadRoutes = APIRouter()

# class ResponseModel(BaseModel):
#     data: Union[dict, list]


async def get_api_key(api_key: str):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=400, detail="Invalid API Key")


@threadRoutes.get("/get")
async def get_messages(request: Request):
    await get_api_key(request.headers["api-key"])
    threads = await get_threads()
    print("Threads: ", threads)
    return {"data": threads}


@threadRoutes.post("/create")
async def send_message(request: Request):
    await get_api_key(request.headers["api-key"])
    new_thread = await create_thread()
    return new_thread.model_dump()
