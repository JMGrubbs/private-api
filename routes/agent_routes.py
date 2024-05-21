from fastapi import APIRouter, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# from typing import Optional
from dependencies import validate_api_key, db_session
from agent.data_classes import NewAgent, DeleteAgent
from agent.controller import create_agents, select_agents, delete_agent, retrieve_agents


agentRoutes = APIRouter()


@agentRoutes.post("/refresh-db", dependencies=[Depends(validate_api_key)])
async def agents_db_load(db=Depends(db_session)):
    try:
        await retrieve_agents(db)
        return {"response": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent retrieval failed: {e}")


@agentRoutes.get("/get", dependencies=[Depends(validate_api_key)])
async def get_agents(db=Depends(db_session)):
    try:
        agents = await select_agents(db)
        return {"response": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agents from db: {e}")


@agentRoutes.post("/create", dependencies=[Depends(validate_api_key)])
async def create_new_agent(newAgent: NewAgent, db=Depends(db_session)):
    try:
        new_agent = await create_agents(newAgent, db)
        return {"response": new_agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent creation failed: {e}")


@agentRoutes.delete("/delete", dependencies=[Depends(validate_api_key)])
async def agent_delete(agent: DeleteAgent, db=Depends(db_session)):
    try:
        result = await delete_agent(agent, db)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to delete agent")
        return {"response": "delete agent"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete agent: {e}")
