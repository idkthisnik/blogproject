from backend.logic.models.post import Post
from pydantic import BaseModel


class PostsResponse(BaseModel):
    posts: list[Post] = []
    
class PostResponse(BaseModel):
    post: Post