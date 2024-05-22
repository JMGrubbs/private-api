from fastapi import APIRouter, HTTPException, Request, Depends
from dependencies import validate_api_key, db_session

from messages.controller import get_messages, send_message


messageRoutes = APIRouter()


@messageRoutes.get("/{id}/get", dependencies=[Depends(validate_api_key)])
async def messages_get(id: str):
    try:
        messages = await get_messages(id)
        result = True
        if not result:
            raise HTTPException(status_code=404, detail="No messages found")
        return {"response": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@messageRoutes.post("/add", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def message_send(request: Request, db=Depends(db_session)):
    try:
        request_body = await request.json()
        all_messages = await send_message(request_body, db)
        if not all_messages:
            raise HTTPException(status_code=404, detail="Message not sent")
        return {"response": all_messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
