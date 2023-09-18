from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from backend.logic.models.comment import Comment
from backend.logic.services.comment_service import CommentService
from backend.logic.dtos.requests.comment.createcomment_request import CreateCommentRequest
from backend.logic.dtos.requests.rating.get_comment_rated_by_user_request import GetCommentRatedByUser
from backend.logic.dtos.requests.rating.ratecomment_request import RateCommentRequest
from backend.logic.dtos.requests.comment.deletecomment_request import DeleteCommentRequest
from backend.logic.dtos.requests.comment.updatecomment_request import UpdateCommentRequest


router = APIRouter()

comment_service = CommentService()

@router.get('/posts/{post_id}/comments', response_model=Page[Comment])
def get_comments(post_id):
    result = comment_service.get_comments_for_post(post_id)
    return paginate(result)

@router.post('/posts/{post_id}/create_comment')
def create_comment(data: CreateCommentRequest):
    if len(data.comment_text) == 0:
        raise HTTPException(status_code=422, detail="Comment can not be empty object :D") 
    result = comment_service.create_comment(data)
    return result

@router.post('/posts/{post_id}/commentRatedByUser')
def get_comment_rated_by_user(user_comment_info: GetCommentRatedByUser):
    result = comment_service.comment_rated_by_user(user_comment_info)
    return result

@router.post('/posts/{post_id}/{comment_id}')
def rate_comment(rate_info: RateCommentRequest):
    result = comment_service.rate_comment(rate_info)
    return result

@router.put('/posts/{post_id}/{comment_id}/update')
def update_comment(info: UpdateCommentRequest):
    result = comment_service.update_my_comment(info)
    return result

@router.delete('/posts/{post_id}/{comment_id}')
def delete_comment(data: DeleteCommentRequest):
    result = comment_service.delete_comment(data)
    return result