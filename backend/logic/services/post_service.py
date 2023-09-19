from backend.logic.models.post import Post
from backend.database.crud.posts_crud import PostsCrud
from backend.database.crud.user_crud import UserCrud
from backend.database.crud.comments_crud import CommentsCrud
from backend.database.crud.postsrating_crud import PostsRatingCrud
from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.database.crud.subscriptions_crud import SubscriptionsCrud

from backend.logic.dtos.requests.rating.ratepost_request import RatePostRequest
from backend.logic.dtos.requests.post.createpost_request import CreatePostRequest
from backend.logic.dtos.requests.post.updatepost_request import UpdatePostRequest
from backend.logic.dtos.requests.post.deletepost_request import DeletePostRequest
from backend.logic.dtos.responses.post.posts_response import PostResponse, PostsResponse
from backend.logic.dtos.requests.rating.get_post_rated_by_user_request import GetPostRatedByUser
from backend.logic.dtos.responses.rating.post_rated_by_user_response import PostRatedByUserResponse


s_c = SubscriptionsCrud()
p_c = PostsCrud()
u_c = UserCrud()
c_c = CommentsCrud()
p_r_c = PostsRatingCrud()
c_r_c = CommentsRatingCrud()

class PostService():
    def get_post(self, post_id: int) -> PostResponse:
        post = p_c.get_post(post_id)
        if post:
            post['post_creator'] = u_c.get_login_by_id(post['post_creator_id'])
            post['comments_count'] = c_c.get_comments_count_for_post(post['post_id'])
            post['post_rating'] = p_r_c.get_post_total_rating(post['post_id'])
            return PostResponse(post=post)
        else:
            return post
    
    def get_posts(self, sorted: str) -> PostsResponse:
        if sorted == 'null':
            posts = p_c.get_all_posts(sorted=None)
        else:
            posts = p_c.get_all_posts(int(sorted))
        
        if posts:
            result = []
            for post in posts:
                post['post_creator'] = u_c.get_login_by_id(post['post_creator_id'])
                post['comments_count'] = c_c.get_comments_count_for_post(post['post_id'])
                post['post_rating'] = p_r_c.get_post_total_rating(post['post_id'])
                result.append(Post(**post))
                
            return result
    
    def create_post(self, data: CreatePostRequest) -> dict:
        new_post_id = p_c.create_post(data)
        result = p_c.get_post(new_post_id)
        result['post_creator'] = u_c.get_login_by_id(result['post_creator_id'])
        return result
    
    def post_rated_by_user(self, user_post_info: GetPostRatedByUser) -> PostRatedByUserResponse:
        response = PostRatedByUserResponse()
        if p_r_c.check_post_rating_existence(user_post_info.post_id, user_post_info.user_id):
            response.rating_existence = True
            response.rating_value = p_r_c.get_post_rating_value(user_post_info.post_id, user_post_info.user_id)
        else:
            response.rating_existence = False

        return response
    
   
    def rate_post(self, rate_info: RatePostRequest) -> bool:
        rate_table = {
            'like': 4,
            'dislike': -2
        }
        
        updated_rate_info = RatePostRequest(
            user_id=rate_info.user_id,
            rating_receiver=rate_info.rating_receiver,
            post_id=rate_info.post_id,
            rating_value=rate_table[rate_info.rating_value]
        )
        
        rate_existence = p_r_c.check_post_rating_existence(updated_rate_info.post_id, updated_rate_info.user_id)
        
        if rate_existence:
            if not p_r_c.check_post_rating_by_value(updated_rate_info):
                p_r_c.delete_post_rating(updated_rate_info)
                p_r_c.create_post_rating(updated_rate_info)
            else:
                p_r_c.delete_post_rating(updated_rate_info)
        else:
            p_r_c.create_post_rating(updated_rate_info)
 
        return True
    
    
    def update_my_post(self, new_post: UpdatePostRequest) -> None:
        p_c.update_post(new_post)
    
        
    def delete_my_post(self, info: DeletePostRequest) -> str:
        comments_deleted_id = c_c.get_comments_ids_to_delete(info.post_id)
        
        for comment_id in comments_deleted_id:
            c_r_c.delete_comment_rating(comment_id)
            
        c_c.delete_all_comments_for_post(info.post_id)
        p_r_c.delete_all_post_rating(info.post_id)
        p_c.delete_post(info.post_id, info.user_id)
        
        return 'Succsessfully deleted your post!' 