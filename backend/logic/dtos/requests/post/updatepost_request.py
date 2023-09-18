from pydantic import BaseModel

class UpdatePostRequest(BaseModel):
    user_id: int
    post_id: int
    new_text: str