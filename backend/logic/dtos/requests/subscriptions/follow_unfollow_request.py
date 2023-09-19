from pydantic import BaseModel


class FollowUnfollowRequest(BaseModel):
    user_id: int
    subscriber_id: int 
    