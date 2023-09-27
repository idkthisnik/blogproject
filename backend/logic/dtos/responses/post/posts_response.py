from pydantic import BaseModel
from logic.models.post import Post


class PostsResponse(BaseModel):
    posts: list[Post] = []
    
class PostResponse(BaseModel):
    post: Post