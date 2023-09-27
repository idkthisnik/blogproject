from typing import Annotated
from fastapi_pagination import Page, paginate
from fastapi import APIRouter, HTTPException, Query, Depends

from logic.models.post import Post
from logic.services.post_service import PostService
from logic.dtos.responses.post.posts_response import PostResponse
from logic.dtos.requests.rating.ratepost_request import RatePostRequest
from logic.dtos.requests.post.createpost_request import CreatePostRequest
from logic.dtos.requests.post.updatepost_request import UpdatePostRequest
from logic.dtos.requests.post.deletepost_request import DeletePostRequest
from logic.dtos.requests.rating.get_post_rated_by_user_request import GetPostRatedByUser
from logic.dtos.responses.rating.post_rated_by_user_response import PostRatedByUserResponse


router = APIRouter()

post_service = PostService()

@router.get('/posts/{post_id}/', response_model=PostResponse)
def get_post(post_id: int) -> PostResponse:
    result = post_service.get_post(post_id)
    if not result:
        raise HTTPException(status_code=404, detail='Oops! Post not found!')
    return result


@router.get('/posts/', response_model=Page[Post])
def get_posts(sorted: str = Query(default=None, description='Sorting criteria')) -> Page[Post]:
    result = post_service.get_posts(sorted)
    if not result:
        raise HTTPException(status_code=404, detail='Oops! Posts not found!')
    return paginate(result)

@router.post('/posts/create')
def create_post(data: CreatePostRequest) -> dict:
    if len(data.post_text) == 0:
        raise HTTPException(status_code=422, detail="Comment can not be empty object :D") 
    result = post_service.create_post(data)
    return result

@router.get('/posts/{post_id}/postRatedByUser')
def get_post_rated_by_user(
        user_post_info: Annotated[GetPostRatedByUser, Depends()]
    ) -> PostRatedByUserResponse:
    result = post_service.post_rated_by_user(user_post_info)
    return result

@router.post('/posts/{post_id}/rate')
def rate_post(rate_info: RatePostRequest) -> bool:
    result = post_service.rate_post(rate_info)
    return result

@router.put('/posts/{post_id}/update')
def update_post(info: UpdatePostRequest) -> None:
    result = post_service.update_my_post(info)
    return result

@router.delete('/posts/{post_id}/delete')
def delete_post(info: DeletePostRequest) -> str:
    result = post_service.delete_my_post(info)
    return result