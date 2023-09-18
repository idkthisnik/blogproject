from pydantic import BaseModel, EmailStr

class MPUserDataResponse(BaseModel):
    login: str
    email: EmailStr
    rating: int
    subscriptions: int
    subscribers: int
    
class UserDataResponse(BaseModel):
    login: str
    rating: int
    subscriptions: int
    subscribers: int