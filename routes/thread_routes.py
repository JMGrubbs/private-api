from fastapi import APIRouter, HTTPException, Depends
from dependencies import validate_api_key, db_session
from threads.controller import create_thread, select_threads, delete_thread


threadRoutes = APIRouter()


@threadRoutes.get("/get", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def threads_select(db=Depends(db_session)):
    try:
        threads = await select_threads(db)
        if len(threads) > 0:
            raise HTTPException(status_code=404, detail="Error getting threads")
        return {"response": threads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@threadRoutes.post("/create", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def threads_create(db=Depends(db_session)):
    try:
        new_thread = await create_thread(db)
        if not new_thread:
            raise HTTPException(status_code=500, detail="Thread not created")
        return {"response": new_thread}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@threadRoutes.delete("/{thread_id}/delete", dependencies=[Depends(validate_api_key), Depends(db_session)])
async def threads_delete(thread_id: int, db=Depends(db_session)):
    try:
        result = await delete_thread(db, thread_id)
        print(result)
        if not result:
            raise HTTPException(status_code=404, detail="Thread not found")
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
