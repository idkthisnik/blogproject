from pydantic import BaseModel, EmailStr

    
class UserDataResponse(BaseModel):
    login: str
    profile_page: str
    rating: int
    subscriptions: int
    subscribers: int