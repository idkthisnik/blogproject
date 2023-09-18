from fastapi import HTTPException

from fastapi import APIRouter
from backend.logic.services.userpage_service import UserProfileService
from backend.logic.dtos.requests.rating.ratepost_request import RatePostRequest
from backend.logic.dtos.requests.subscriptions.follow_unfollow_request import *


userprofile_service = UserProfileService()
router = APIRouter()


@router.get('/{user_id}/data')
def get_user_data(user_id):
    result = userprofile_service.get_user_data(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.get('/users')
def get_users():
    result = userprofile_service.get_users()
    print(result)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result