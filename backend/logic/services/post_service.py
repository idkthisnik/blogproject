from backend.database.crud.posts_crud import PostsCrud
from backend.database.crud.user_crud import UserCrud
from backend.database.crud.comments_crud import CommentsCrud
from backend.database.crud.postsrating_crud import PostsRatingCrud
from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.database.crud.subscriptions_crud import SubscriptionsCrud

from backend.logic.dtos.responses.post.posts_response import PostResponse, PostsResponse
from backend.logic.models.post import Post
from backend.logic.dtos.responses.rating.post_rated_by_user_response import PostRatedByUserResponse
from backend.logic.dtos.requests.rating.ratepost_request import RatePostRequest

subscriptions_crud = SubscriptionsCrud()
posts_crud = PostsCrud()
users_crud = UserCrud()
comments_crud = CommentsCrud()
posts_rating_crud = PostsRatingCrud()
comments_rating_crud = CommentsRatingCrud()

class PostService():
    def get_post(self, post_id) -> PostResponse:
        
        post = posts_crud.get_post_by_postid(post_id)
        if post:
            post['post_creator'] = users_crud.get_login_by_id(post['post_creator_id'])
            post['comments_count'] = comments_crud.get_comment_count_by_postid(post['post_id'])
            post['post_rating'] = posts_rating_crud.get_post_rating_by_postid(post['post_id'])
    
            return PostResponse(post=post)
        else:
            return post
    
    
    def get_posts(self, sorted) -> PostsResponse:
        if sorted == 'null':
            posts = posts_crud.get_all_posts(sorted=None)
        else:
            posts = posts_crud.get_all_posts(int(sorted))
        
        if posts:
            result = []
            for post in posts:
                post['post_creator'] = users_crud.get_login_by_id(post['post_creator_id'])
                post['comments_count'] = comments_crud.get_comment_count_by_postid(post['post_id'])
                post['post_rating'] = posts_rating_crud.get_post_rating_by_postid(post['post_id'])
                result.append(Post(**post))
                
            return result
    
    
    def create_the_post(self, data):
        new_post_id = posts_crud.create_post(data)
        result = posts_crud.get_post_by_postid(new_post_id)
        result['post_creator'] = users_crud.get_login_by_id(result['post_creator_id'])
        return result
    
    
    def post_rated_by_user(self, user_post_info) -> PostRatedByUserResponse:
        response = PostRatedByUserResponse()
        if posts_rating_crud.check_rating_existence(user_post_info.post_id, user_post_info.user_id):
            response.rating_existence = True
            response.rating_value = posts_rating_crud.get_rating_value(user_post_info.post_id, user_post_info.user_id)
        else:
            response.rating_existence = False

        return response
    
   
    def rate_post(self, rate_info) -> bool:
        rate_table = {'like': 4,
                      'dislike': -2}
        
        updated_rate_info = RatePostRequest(
                user_id=rate_info.user_id,
                rating_receiver=rate_info.rating_receiver,
                post_id=rate_info.post_id,
                rating_value=rate_table[rate_info.rating_value]
    )
        
        rate_existence = posts_rating_crud.rate_existence(updated_rate_info)
        
        if rate_existence:
            if not posts_rating_crud.rate_existence_by_value(updated_rate_info):
                posts_rating_crud.delete_rating(updated_rate_info)
                posts_rating_crud.create_post_rating(updated_rate_info)
            else:
                posts_rating_crud.delete_rating(updated_rate_info)
        else:
            posts_rating_crud.create_post_rating(updated_rate_info)
 
        return True
    
    
    def update_my_post(self, new_post):
        posts_crud.update_post(new_post)
    
        
    def delete_my_post(self, info):
        comments_deleted_id = comments_crud.get_comments_id_to_delete(info.post_id)
        for comment_id in comments_deleted_id:
            comments_rating_crud.delete_comment_rating_by_commentid(comment_id)
        comments_crud.delete_all_comments_by_postid(info.post_id)
        posts_rating_crud.delete_all_ratings_by_post_id(info.post_id)
        posts_crud.delete_post(info.post_id, info.user_id)
        return 'Succsessfully deleted your post!'
    
    def delete_post_rating(self, post_rating) -> bool:
        posts_rating_crud.delete_post_rating_by_id(post_rating.user_id, post_rating.post_id)
        return True     