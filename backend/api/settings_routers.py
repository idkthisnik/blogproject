import os
from PIL import Image
import secrets
from fastapi import UploadFile, APIRouter, HTTPException

from logic.services.settings_service import SettingsService
from logic.dtos.requests.settings.updatelogin_request import UpdateLoginRequest
from logic.dtos.requests.settings.updateemail_request import UpdateEmailRequest
from logic.dtos.requests.settings.deleteaccount_request import DeleteProfileRequest
from logic.dtos.requests.settings.updatepassword_request import UpdatePasswordRequest
from logic.dtos.requests.settings.deleteprofileimage_request import DeleteProfilePageRequest
from logic.dtos.requests.settings.changeprofilepage_request import ChangeProfilePageRequest


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

@router.post("/my_profile/uploadimage/")
async def create_upload_file(user_id: int, file: UploadFile) -> dict:
    file_format = file.filename.split('.')[1]
    if file_format not in ['png', 'jpg', 'jpeg']:
        raise HTTPException(status_code=422, detail="File extension not allowed!")
    
    FILEPATH = "./static/images/"
    file_hex_name = f'{secrets.token_hex(10)}.{file_format}'
    generated_name = FILEPATH + file_hex_name
    file_content = await file.read()
    
    data = ChangeProfilePageRequest(user_id=user_id, profile_image=file_hex_name)
    settings_service.change_profile_image(data)
    
    with open(generated_name, "wb") as file_to_fill:
        file_to_fill.write(file_content)
        
    im = Image.open(generated_name)
    im = im.resize((128, 128))
    im.save(generated_name)
    
    await file.close()
    
    file_url = f"{os.environ['FASTAPI_DOMAIN']}/static/images/{file_hex_name}"
    
    return {'status': 200, 'file': file_url}

@router.delete("/my_profile/deleteimage/")
def delete_profile_image(data: DeleteProfilePageRequest):
    return settings_service.delete_profile_image(data)