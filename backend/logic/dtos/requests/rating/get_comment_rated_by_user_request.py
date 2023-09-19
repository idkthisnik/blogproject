from pydantic import BaseModel


class GetCommentRatedByUser(BaseModel):
    comment_id: int
    user_id: int