from pydantic import BaseModel


class DeleteCommentRequest(BaseModel):
    user_id: int
    comment_id: int