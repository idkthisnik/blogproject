from fastapi import HTTPException
from fastapi import APIRouter

from backend.logic.services.settings_service import SettingsService
from backend.logic.dtos.requests.settings.updatelogin_request import UpdateLoginRequest
from backend.logic.dtos.requests.settings.updateemail_request import UpdateEmailRequest
from backend.logic.dtos.requests.settings.deleteaccount_request import DeleteProfileRequest
from backend.logic.dtos.requests.settings.updatepassword_request import UpdatePasswordRequest


settings_service = SettingsService()
router = APIRouter()


@router.put('/my_profile/settings/change_login')
def change_login(data: UpdateLoginRequest) -> bool | None:
    result = settings_service.update_login(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Data is not valid!")
    return result

@router.put('/my_profile/settings/change_password')
def change_password(data: UpdatePasswordRequest) -> bool | None:
    result = settings_service.update_password(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Data is not valid!")
    return result

@router.put('/my_profile/settings/change_email')
def change_email(data: UpdateEmailRequest) -> bool | None:
    result = settings_service.update_email(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Data is not valid!")
    return result

@router.delete('/my_profile/settings/delete_account')
def delete_profile(data: DeleteProfileRequest) -> bool | None:
    result = settings_service.delete_account(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Data is not valid!")
    return result