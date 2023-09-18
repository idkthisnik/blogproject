from pydantic import BaseModel


class RatePostRequest(BaseModel):
    user_id: int
    rating_receiver: int
    post_id: int
    rating_value: str | int