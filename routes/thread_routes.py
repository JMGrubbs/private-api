from fastapi import APIRouter, HTTPException, Depends
from dependencies import validate_api_key, db_session
from threads.controller import create_thread, select_threads, delete_thread


threadRoutes = APIRouter()


@threadRoutes.get("/get", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def threads_select(db=Depends(db_session)):
    threads = await select_threads(db)
    result = True
    if not result:
        raise HTTPException(status_code=404, detail="Error getting threads")
    return {"response": threads}


@threadRoutes.post("/create", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def threads_create(db=Depends(db_session)):
    new_thread = await create_thread(db)
    if not new_thread:
        raise HTTPException(status_code=500, detail="Thread not created")
    return {"response": new_thread}


@threadRoutes.delete(
    "/{thread_id}/delete", dependencies=[Depends(validate_api_key), Depends(db_session)]
)
async def threads_delete(thread_id: str, db=Depends(db_session)):
    result = await delete_thread(db, thread_id)
    if not result:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"response": result}
