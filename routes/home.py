from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os

api_key = os.getenv("API_KEY")


homeRoutes = APIRouter()


class ResponseModel(BaseModel):
    response: dict


async def get_api_key(api_key: str):
    if api_key == api_key:
        return api_key
    else:
        raise HTTPException(status_code=400, detail="Invalid API Key")


@homeRoutes.get("/", tags=["home"], response_model=ResponseModel)
async def get_messages(request: Request):
    await get_api_key(request.headers["api-key"])

    return {"response": {"temp": "Message sent successfully"}}
