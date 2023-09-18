from pydantic import BaseModel



class Comment(BaseModel):
    comment_id: int
    creator_id: int
    comment_text: str
    comment_time: str 
    comment_creator: str 
    comment_rating: int 