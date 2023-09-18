from pydantic import BaseModel

class GetPostRatedByUser(BaseModel):
    post_id: int
    user_id: int