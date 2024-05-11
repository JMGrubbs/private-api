from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependencies import validate_api_key

homeRoutes = APIRouter()


class ResponseModel(BaseModel):
    response: dict


# response_model=ResponseModel,


@homeRoutes.get("/home", tags=["home"], dependencies=[Depends(validate_api_key)])
async def get_messages():
    return {"response": {"temp": "Hello World"}}


@homeRoutes.get("/test", tags=["test"])
async def test_sight():
    return {"response": {"temp": "API is up!!"}}
