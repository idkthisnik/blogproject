from pydantic import BaseModel

class DeletePostRatingRequest(BaseModel):
    user_id: int
    post_id: int