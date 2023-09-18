from pydantic import BaseModel, EmailStr

class RegistrationRequestToDB(BaseModel):
    username: str
    password: str
    email: EmailStr
    salt: str
    
class LoginRequestToDB(BaseModel):
    username: str
    password: str