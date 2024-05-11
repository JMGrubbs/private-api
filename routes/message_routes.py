from fastapi import APIRouter, HTTPException, Request, Depends
from dependencies import validate_api_key


messageRoutes = APIRouter()


@messageRoutes.get("/get", tags=["messages"], dependencies=[Depends(validate_api_key)])
async def get_messages(request: Request):
    # json_messages = [
    #     message.model_dump() for message in proxy_agent.messages
    # ]
    # print(json_messages)
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="No messages found")

    return {"data": ["messages"]}


@messageRoutes.get("/sendmessage", tags=["messages"], dependencies=[Depends(validate_api_key)])
async def send_message(request: Request):
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="Message not sent")
    return {"response": {"temp": "Message sent successfully"}}
