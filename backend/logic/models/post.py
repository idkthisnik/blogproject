from pydantic import BaseModel


class Post(BaseModel):
    post_id: int
    post_creator_id: int 
    post_text: str 
    post_time: str 
    post_creator: str 
    comments_count: int
    post_rating: int 