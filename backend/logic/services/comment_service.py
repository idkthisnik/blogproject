from typing import List

from backend.logic.models.comment import Comment
from backend.database.crud.user_crud import UserCrud
from backend.database.crud.comments_crud import CommentsCrud
from backend.database.crud.commentsrating_crud import CommentsRatingCrud
from backend.logic.dtos.requests.rating.ratecomment_request import RateCommentRequest
from backend.logic.dtos.requests.comment.updatecomment_request import UpdateCommentRequest
from backend.logic.dtos.requests.comment.deletecomment_request import DeleteCommentRequest
from backend.logic.dtos.requests.comment.createcomment_request import CreateCommentRequest
from backend.logic.dtos.requests.rating.get_comment_rated_by_user_request import GetCommentRatedByUser
from backend.logic.dtos.responses.rating.comment_rated_by_user_response import CommentRatedByUserResponse


u_c = UserCrud()
c_c = CommentsCrud()
c_r_c = CommentsRatingCrud()

class CommentService():
    def create_comment(self, data: CreateCommentRequest) -> dict:
        new_comment_id = c_c.create_comment(data)
        result = c_c.get_comment(new_comment_id)
        result['comment_creator'] = u_c.get_login_by_id(result['creator_id'])
        return result
    
    def get_comments_for_post(self, post_id: int) -> List[Comment]:
        comments = c_c.get_comments_for_post(post_id)
        result = []
        for comment in comments:
            comment['comment_creator'] = u_c.get_login_by_id(comment['creator_id'])
            comment['comment_rating'] = c_r_c.get_comment_total_rating(comment['comment_id'])
                
            result.append(Comment(**comment))
                
        return result
        
    def rate_comment(self, rate_info: RateCommentRequest) -> bool:
        rate_table = {
            'like': 4,
            'dislike': -2
        }
            
        updated_rate_info = RateCommentRequest(
            user_id=rate_info.user_id,
            rating_receiver=rate_info.rating_receiver,
            comment_id=rate_info.comment_id,
            rating_value=rate_table[rate_info.rating_value]
        )
            
        rate_existence = c_r_c.check_comment_rating_existence(updated_rate_info)
        
        if rate_existence:
            if not c_r_c.check_comment_rating_by_value(updated_rate_info):
                c_r_c.delete_comment_rating(updated_rate_info)
                c_r_c.create_comment_rating(updated_rate_info)
            else:
                c_r_c.delete_comment_rating(updated_rate_info)
        else:
            c_r_c.create_comment_rating(updated_rate_info)

        return True

    def comment_rated_by_user(self, user_comment_info: GetCommentRatedByUser) -> CommentRatedByUserResponse:
        response = CommentRatedByUserResponse()
        if c_r_c.check_comment_rating_existence(user_comment_info):
            response.rating_existence = True
            response.rating_value = c_r_c.get_comment_rating_value(user_comment_info.comment_id, user_comment_info.user_id)
        else:
            response.rating_existence = False

        return response
        
    def update_my_comment(self, data: UpdateCommentRequest) -> None:
        c_c.update_comment(data)
        
    def delete_comment(self, data: DeleteCommentRequest) -> None:
        c_r_c.delete_comment_rating(data.comment_id)
        c_c.delete_comment(data)