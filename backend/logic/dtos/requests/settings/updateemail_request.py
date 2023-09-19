from pydantic import BaseModel, EmailStr


class UpdateEmailRequest(BaseModel):
    login: str
    password: str
    new_email: EmailStr