from pydantic import BaseModel
from typing import Optional


class NewAgent(BaseModel):
    agentName: str
    agentDescription: str
    agentInstructions: str
    model: str


class DeleteAgent(BaseModel):
    agent_id: str
    description: Optional[str]
    instructions: str
    model: str
    name: str
