from pydantic import BaseModel
from logic.models.comment import Comment


class CommentsResponse(BaseModel):
    comments: list[Comment] = []