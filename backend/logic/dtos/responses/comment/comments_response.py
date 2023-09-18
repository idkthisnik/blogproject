from backend.logic.models.comment import Comment
from pydantic import BaseModel


class CommentsResponse(BaseModel):
    comments: list[Comment] = []