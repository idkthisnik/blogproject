from pydantic import BaseModel

class CreateCommentRequest(BaseModel):
    user_id: int 
    post_id: int  
    comment_text: str