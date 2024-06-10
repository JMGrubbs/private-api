from pydantic import BaseModel
from typing import Optional

class AppValidation(BaseModel):
    name: Optional[str] = "new validation"
    password: str

class RevokedValidation(BaseModel):
    name: str
    revoked: bool