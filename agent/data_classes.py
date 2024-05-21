from pydantic import BaseModel


class NewAgent(BaseModel):
    agentName: str
    agentDescription: str
    agentInstructions: str
    model: str
