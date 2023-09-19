from pydantic import BaseModel


class RateCommentRequest(BaseModel):
    user_id: int
    rating_receiver: int
    comment_id: int
    rating_value: str | int