from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from typing import Annotated, Any

from logic.models.comment import Comment
from logic.services.comment_service import CommentService
from logic.dtos.requests.rating.ratecomment_request import RateCommentRequest
from logic.dtos.requests.comment.deletecomment_request import DeleteCommentRequest
from logic.dtos.requests.comment.updatecomment_request import UpdateCommentRequest
from logic.dtos.requests.comment.createcomment_request import CreateCommentRequest
from logic.dtos.requests.rating.get_comment_rated_by_user_request import GetCommentRatedByUser
from logic.dtos.responses.rating.comment_rated_by_user_response import CommentRatedByUserResponse


router = APIRouter()

comment_service = CommentService()

@router.get('/posts/{post_id}/comments', response_model=Page[Comment])
def get_comments(post_id) -> Page[Comment]:
    result = comment_service.get_comments_for_post(post_id)
    return paginate(result)

@router.post('/posts/{post_id}/create_comment')
def create_comment(data: CreateCommentRequest) -> dict:
    if len(data.comment_text) == 0:
        raise HTTPException(status_code=422, detail="Comment can not be empty object :D") 
    result = comment_service.create_comment(data)
    return result

@router.get('/posts/{post_id}/commentRatedByUser')
def get_comment_rated_by_user(
        user_comment_info: Annotated[GetCommentRatedByUser, Depends()]
    ) -> CommentRatedByUserResponse:
    result = comment_service.comment_rated_by_user(user_comment_info)
    return result

@router.post('/posts/{post_id}/{comment_id}')
def rate_comment(rate_info: RateCommentRequest) -> bool:
    result = comment_service.rate_comment(rate_info)
    return result

@router.put('/posts/{post_id}/{comment_id}/update')
def update_comment(info: UpdateCommentRequest) -> None:
    result = comment_service.update_my_comment(info)
    return result

@router.delete('/posts/{post_id}/{comment_id}')
def delete_comment(data: DeleteCommentRequest) -> None:
    result = comment_service.delete_comment(data)
    return result