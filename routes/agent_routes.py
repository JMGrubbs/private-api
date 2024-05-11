from fastapi import APIRouter, HTTPException, Request, Depends, Query
from typing import Optional
from dependencies import validate_api_key
from agent.controller import get_agents


agentRoutes = APIRouter()


@agentRoutes.get("/", dependencies=[Depends(validate_api_key)])
async def retrieve_agents(agent_id: Optional[str] = Query(None, alias="agent-id")):
    try:
        agents = await get_agents(agent_id)
        return {"response": agents}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Agent retrieval failed: {e}")


@agentRoutes.get("/proxy/messages", dependencies=[Depends(validate_api_key)])
async def add_proxy_message(request: Request):
    global proxy_agent
    if proxy_agent is None:
        return {"Status": False}
    return {"data": proxy_agent.messages}
