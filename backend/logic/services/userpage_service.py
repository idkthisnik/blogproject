from backend.database.crud.subscriptions_crud import SubscriptionsCrud
from backend.database.crud.user_crud import UserCrud
from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.database.crud.postsrating_crud import PostsRatingCrud
from backend.database.crud.comments_crud import CommentsCrud
from backend.logic.dtos.responses.profile.userdata_response import UserDataResponse


subscriptions_crud = SubscriptionsCrud()
comments_crud = CommentsCrud()
users_crud = UserCrud()
postsrating_crud = PostsRatingCrud()
commentsrating_crud = CommentsRatingCrud()

class UserProfileService():
    def get_user_data(self, user_id) -> UserDataResponse: 
        responsedb = users_crud.get_user_by_id(user_id)
        if responsedb:
            user_data = {'login': responsedb['login']}
            user_data['rating'] = postsrating_crud.get_user_posts_rating_by_id(
                                user_id
                                ) + commentsrating_crud.get_user_comments_rating_by_id(user_id)
            user_data['subscriptions'] = subscriptions_crud.get_subscriptions_count(user_id) 
            user_data['subscribers'] = subscriptions_crud.get_subscribers_count(user_id)
        
            return UserDataResponse(**user_data)
        
        else:
            return None
        
    def get_users(self):
        return users_crud.get_all_users()
        
