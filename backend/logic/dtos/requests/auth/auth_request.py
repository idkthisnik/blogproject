from pydantic import BaseModel, EmailStr, Field


class RegistrationRequest(BaseModel):
    username: str = Field(min_length=4, max_length=16, 
                          pattern=r'^[a-zA-Z_][a-zA-Z0-9_-]{3,15}$'
                          )
    entered_password: str = Field(min_length=8, max_length=32, 
                          pattern=r"^[a-zA-Z][a-zA-Z0-9]{7,31}$"
                          )
    email: EmailStr
    
    
class LoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=16, 
                          pattern=r'^[a-zA-Z_][a-zA-Z0-9_-]{3,15}$'
                          )
    entered_password: str = Field(min_length=8, max_length=32, 
                          pattern=r"^[a-zA-Z][a-zA-Z0-9]{7,31}$"
                          )
    
class RefreshRequest(BaseModel):
    user_id: int
    refresh_token: str
    
    
class LogoutRequest(BaseModel):
    user_id: int