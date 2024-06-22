from pydantic import BaseModel
from sqlalchemy.sql import text


class UserSession(BaseModel):
    session_id: str = None
    password: str
    active_status: bool = False

    async def validate_session(self, db):
        stmt = text("SELECT id, name FROM chatbot.app_validation WHERE temp_pass = :temp_pass AND cur_status = 'true'")
        try:
            async with db as session:
                valid = await session.execute(stmt, {"temp_pass": self.password})
                print("from the database:", valid)
                valid = [
                    {
                        "id": id,
                        "name": user_name,
                    }
                    for id, user_name in valid
                ]
                if valid:
                    user = valid[0]
                    self.session_id = str(user["id"]) + ":" + user["name"]
                    self.active_status = True
                return True
        except Exception as e:
            print(e)
            return []
