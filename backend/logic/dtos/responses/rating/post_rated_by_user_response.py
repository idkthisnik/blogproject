from pydantic import BaseModel


class PostRatedByUserResponse(BaseModel):
    rating_existence: bool = None
    rating_value: int = None