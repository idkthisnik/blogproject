from pydantic import BaseModel


class ChangeProfilePageRequest(BaseModel):
    user_id: int
    profile_image: str