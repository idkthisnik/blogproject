from typing import List
from fastapi import APIRouter
from fastapi import HTTPException

from logic.services.userpage_service import UserProfileService
from logic.dtos.responses.profile.userdata_response import UserDataResponse

router = APIRouter()

userprofile_service = UserProfileService()


@router.get('/{user_id}/data')
def get_user_data(user_id: int) -> UserDataResponse:
    result = userprofile_service.get_user_data(user_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return result

@router.get('/users')
def get_users() -> List[dict]:
    result = userprofile_service.get_users()
    print(result)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return result