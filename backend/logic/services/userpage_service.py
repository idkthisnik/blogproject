from typing import List

from backend.database.crud.user_crud import UserCrud
from backend.database.crud.postsrating_crud import PostsRatingCrud
from backend.database.crud.subscriptions_crud import SubscriptionsCrud
from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.logic.dtos.responses.profile.userdata_response import UserDataResponse


s_c = SubscriptionsCrud()
u_c = UserCrud()
p_r_c = PostsRatingCrud()
c_r_c = CommentsRatingCrud()

class UserProfileService():
    def get_user_data(self, user_id: int) -> UserDataResponse: 
        responsedb = u_c.get_user_by_id(user_id)
        if responsedb:
            user_data = {'login': responsedb['login']}
            user_data['rating'] = p_r_c.get_user_total_posts_rating(user_id
                              ) + c_r_c.get_user_total_comments_rating(user_id)
            user_data['subscriptions'] = s_c.get_subscriptions_count(user_id) 
            user_data['subscribers'] = s_c.get_subscribers_count(user_id)
        
            return UserDataResponse(**user_data)
        
        else:
            return None
        
    def get_users(self) -> List[dict]:
        return u_c.get_all_users()