from pydantic import BaseModel, Field


class UpdatePasswordRequest(BaseModel):
    login: str
    password: str
    new_password: str = Field(min_length=8, max_length=32, 
                          pattern=r"^[a-zA-Z][a-zA-Z0-9]{7,31}$"
                          )
    
class UpdatePasswordRequestToDB(BaseModel):
    login: str
    password: str
    new_password: str