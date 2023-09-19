from pydantic import BaseModel


class CommentRatedByUserResponse(BaseModel):
    rating_existence: bool = None
    rating_value: int = None