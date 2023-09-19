from pydantic import BaseModel


class UpdateCommentRequest(BaseModel):
    user_id: int
    comment_id: int
    new_text: str