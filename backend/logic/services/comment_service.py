from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.database.crud.comments_crud import CommentsCrud
from backend.database.crud.user_crud import UserCrud

from backend.logic.dtos.requests.rating.ratecomment_request import RateCommentRequest
from backend.logic.dtos.responses.rating.comment_rated_by_user_response import CommentRatedByUserResponse
from backend.logic.dtos.responses.comment.comments_response import CommentsResponse
from backend.logic.models.comment import Comment


users_crud = UserCrud()
comments_crud = CommentsCrud()
comments_rating_crud = CommentsRatingCrud()

class CommentService():
    def create_comment(self, data):
        new_comment_id = comments_crud.create_comment(data)
        result = comments_crud.get_comment_info_by_id(new_comment_id)
        result['comment_creator'] = users_crud.get_login_by_id(result['creator_id'])
        return result
    
    
    def get_comments_for_post(self, post_id):
        comments = comments_crud.get_comments_by_postid(post_id)
        result = []
        for comment in comments:
            comment['comment_creator'] = users_crud.get_login_by_id(comment['creator_id'])
            comment['comment_rating'] = comments_rating_crud.get_comment_rating_by_comment_id(comment['comment_id'])
                
            result.append(Comment(**comment))
                
        return result
        
        
    def rate_comment(self, rate_info) -> bool:
            rate_table = {'like': 4,
                        'dislike': -2}
            
            updated_rate_info = RateCommentRequest(
                    user_id=rate_info.user_id,
                    rating_receiver=rate_info.rating_receiver,
                    comment_id=rate_info.comment_id,
                    rating_value=rate_table[rate_info.rating_value]
                    )
            
            rate_existence = comments_rating_crud.check_rating_existence(updated_rate_info)
            
            if rate_existence:
                if not comments_rating_crud.rate_existence_by_value(updated_rate_info):
                    comments_rating_crud.delete_rating(updated_rate_info)
                    comments_rating_crud.create_comment_rating(updated_rate_info)
                else:
                    comments_rating_crud.delete_rating(updated_rate_info)
            else:
                comments_rating_crud.create_comment_rating(updated_rate_info)
    
            return True

    def comment_rated_by_user(self, user_comment_info) -> CommentRatedByUserResponse:
            response = CommentRatedByUserResponse()
            if comments_rating_crud.check_rating_existence(user_comment_info):
                response.rating_existence = True
                response.rating_value = comments_rating_crud.get_rating_value(user_comment_info.comment_id, user_comment_info.user_id)
            else:
                response.rating_existence = False

            return response
        
    
    def update_my_comment(self, data):
        comments_crud.update_comment(data)
                
        
    def delete_comment(self, data):
        comments_rating_crud.delete_comment_rating_by_commentid(data.comment_id)
        comments_crud.delete_comment(data)