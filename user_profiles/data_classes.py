from pydantic import BaseModel
from sessions.data_classes import UserSession


class UserProfile(BaseModel):
    id: int = None
    name: str = None
    session: str = None

    def __init__(self, password, db):
        new_session = UserSession(password=password, db=db)
        # self.session = new_session
        print(password)
