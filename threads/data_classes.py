from pydantic import BaseModel
from sqlalchemy.sql import text


class Thread(BaseModel):
    id: int
    name: str
    thread_id: str
    status: bool

    async def updateName(self, new_name, db):
        stmtSql = text(f"UPDATE chatbot.threads SET name = {new_name}")
        async with db as session:
            result = await session.execute(stmtSql)
        self.name = new_name
        return True

    async def updateStatus(self, new_staus: bool):
        self.status = new_staus
        return True
