from fastapi import APIRouter, HTTPException, Request, Depends
from dependencies import validate_api_key, db_session

from messages.controller import get_messages, send_message


messageRoutes = APIRouter()


@messageRoutes.get("/{id}/get", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def messages_get(id: int, db=Depends(db_session)):
    messages = await get_messages(id, db)
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="No messages found")
    return {"response": messages}


@messageRoutes.post("/add", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def message_send(request: Request, db=Depends(db_session)):
    request_body = await request.json()
    message_replay = await send_message(request_body, db)
    if not message_replay:
        raise HTTPException(status_code=404, detail="Message not sent")
    return {"response": message_replay}
