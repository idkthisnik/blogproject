from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    user_id: int
    post_text: str 