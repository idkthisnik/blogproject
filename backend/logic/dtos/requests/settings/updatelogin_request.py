from pydantic import BaseModel, Field

class UpdateLoginRequest(BaseModel):
    login: str
    password: str
    new_login: str = Field(min_length=4, max_length=16, 
                          pattern=r'^[a-zA-Z_][a-zA-Z0-9_-]{3,15}$'
                          )