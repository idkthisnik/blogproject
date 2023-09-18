from pydantic import BaseModel

class DeleteProfileRequest(BaseModel):
    login: str
    password: str