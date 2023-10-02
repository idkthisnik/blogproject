from fastapi import APIRouter, HTTPException
from logic.services.subscription_service import SubscriptionsService
from logic.dtos.requests.subscriptions.follow_unfollow_request import FollowUnfollowRequest

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"]
)


subscriptions_service = SubscriptionsService()


@router.get('/subscribers')
def get_subscribers(user_id: int) -> dict:
    result = subscriptions_service.get_subscribers(user_id)
    if not result: 
        raise HTTPException(
            status_code=404,
            detail='Oops! No subscribers founded.'
        )
        
    return result

@router.get('/subscriptions')
def get_subscriptions(user_id: int) -> dict:
    result = subscriptions_service.get_subscriptions(user_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail='Oops! No subscriptions founded.'
        )
        
    return result

@router.post('/follow-unfollow')
def follow_unfollow(data: FollowUnfollowRequest) -> bool:
    result = subscriptions_service.subscribe_unsubscribe(data)
    return result

@router.post('/follow-unfollow/is-followed')
def is_followed(data: FollowUnfollowRequest) -> bool:
    result = subscriptions_service.is_followed(data)
    return result