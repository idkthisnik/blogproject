from fastapi import APIRouter, HTTPException
router = APIRouter()

from backend.logic.services.subscription_service import SubscriptionsService
from backend.logic.dtos.requests.subscriptions.follow_unfollow_request import FollowUnfollowRequest

subscriptions_service = SubscriptionsService()

@router.get('/subscription/subscribers')
def get_subscribers(user_id):
    result = subscriptions_service.get_subscribers(user_id)
    if not result: 
        raise HTTPException(status_code=404, detail='Oops! No subscribers founded.')
    return result

@router.get('/subscription/subscriptions')
def get_subscriptions(user_id):
    result = subscriptions_service.get_subscriptions(user_id)
    if not result:
        raise HTTPException(status_code=404, detail='Oops! No subscriptions founded.')
    return result

@router.post('/subscription/follow-unfollow')
def follow_unfollow(data: FollowUnfollowRequest):
    result = subscriptions_service.subscribe_unsubscribe(data)
    return result

@router.post('/subscription/follow-unfollow/is-followed')
def is_followed(data: FollowUnfollowRequest):
    result = subscriptions_service.is_followed(data)
    return result