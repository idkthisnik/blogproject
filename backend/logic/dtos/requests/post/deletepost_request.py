from pydantic import BaseModel

class DeletePostRequest(BaseModel):
    user_id: int
    post_id: int