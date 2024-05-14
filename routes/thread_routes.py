from fastapi import APIRouter, HTTPException, Depends, Query
from dependencies import validate_api_key, db_session
from typing import Optional
from threads.tools import (
    create_thread,
)
from threads.controller import get_proxy_threads


threadRoutes = APIRouter()


@threadRoutes.get(
    "/", tags=["threads"], dependencies=[Depends(validate_api_key), Depends(db_session)]
)
async def fetch_threads(
    proxy_agent_id: Optional[str] = Query(None, alias="agent-id"), db=Depends(db_session)
):
    threads = await get_proxy_threads(db, proxy_agent_id)
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="No threads found")
    return {"response": threads}


@threadRoutes.post("/create", tags=["threads"], dependencies=[Depends(validate_api_key)])
async def send_message():
    new_thread = await create_thread()
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="Thread not created")
    return new_thread.model_dump()
