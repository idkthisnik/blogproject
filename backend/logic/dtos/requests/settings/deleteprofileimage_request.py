from pydantic import BaseModel


class DeleteProfilePageRequest(BaseModel):
    user_id: int
    profile_image: str