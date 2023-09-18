from pydantic import BaseModel

class GetMyProfileRequest(BaseModel):
    user_id: int
    