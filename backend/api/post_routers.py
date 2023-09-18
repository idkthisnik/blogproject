from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page, paginate

from backend.logic.models.post import Post
from backend.logic.services.post_service import PostService
from backend.logic.dtos.requests.rating.get_post_rated_by_user_request import GetPostRatedByUser
from backend.logic.dtos.responses.post.posts_response import PostResponse, PostsResponse
from backend.logic.dtos.requests.rating.ratepost_request import RatePostRequest
from backend.logic.dtos.requests.post.createpost_request import CreatePostRequest
from backend.logic.dtos.requests.post.updatepost_request import UpdatePostRequest
from backend.logic.dtos.requests.post.deletepost_request import DeletePostRequest


router = APIRouter()

post_service = PostService()

@router.get('/posts/{post_id}/', response_model=PostResponse)
def get_post(post_id):
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
def create_post(data: CreatePostRequest):
    if len(data.post_text) == 0:
        raise HTTPException(status_code=422, detail="Comment can not be empty object :D") 
    result = post_service.create_the_post(data)
    return result

@router.post('/posts/{post_id}/postRatedByUser')
def get_post_rated_by_user(user_post_info: GetPostRatedByUser):
    result = post_service.post_rated_by_user(user_post_info)
    return result

@router.post('/posts/{post_id}/rate')
def rate_post(rate_info: RatePostRequest):
    result = post_service.rate_post(rate_info)
    return result

@router.put('/posts/{post_id}/update')
def update_post(info: UpdatePostRequest):
    result = post_service.update_my_post(info)
    return result

@router.delete('/posts/{post_id}/delete')
def delete_post(info: DeletePostRequest):
    result = post_service.delete_my_post(info)
    return result