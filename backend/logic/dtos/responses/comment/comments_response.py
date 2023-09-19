from pydantic import BaseModel
from backend.logic.models.comment import Comment


class CommentsResponse(BaseModel):
    comments: list[Comment] = []