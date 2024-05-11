from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from dependencies import worker

from routes.home import homeRoutes
from routes.message_routes import messageRoutes
from routes.thread_routes import threadRoutes
from routes.agent_routes import agentRoutes
from agent.controller import get_agents


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    worker_task = asyncio.create_task(worker())
    await get_agents()
    yield
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        print("Worker task was cancelled")


app = FastAPI(lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.prefix = "/api"

app.include_router(agentRoutes, prefix="/agents", tags=["agents"])
app.include_router(homeRoutes, prefix="/home", tags=["home"])
app.include_router(messageRoutes, prefix="/message", tags=["message"])
app.include_router(threadRoutes, prefix="/threads", tags=["threads"])
