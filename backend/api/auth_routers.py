from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from logic.services.auth_service import AuthService
from logic.dtos.requests.auth.auth_request import (
    RegistrationRequest,
    LoginRequest,
    RefreshRequest,
    LogoutRequest
)
from auth.auth_handler import signJWT, decodeJWT

auth_service = AuthService()
router = APIRouter()


@router.post('/registration')
def registrate_user(info: RegistrationRequest) -> JSONResponse:
    reg_request = auth_service.registr_user(info)
    if reg_request == None:
        raise HTTPException(status_code=403, detail="There is a user already created with this login!")
    else:
        user_id = reg_request
        access_token = signJWT(user_id, 600)
        refresh_token = signJWT(user_id, 3600)
        auth_service.add_refresh_to_db(user_id, refresh_token)
        
        response = JSONResponse(content={'userId': user_id, 'access_token': access_token, 'refresh_token': refresh_token})
        return response


@router.post('/login')
def user_login(user: LoginRequest) -> JSONResponse:
    if auth_service.check_user(user):
        user_id = auth_service.get_user_id(user.username)
        
        access_token = signJWT(user_id, 600)
        refresh_token = signJWT(user_id, 3600)
        auth_service.add_refresh_to_db(user_id, refresh_token)
            
        response = JSONResponse(content={'userId': user_id, 'access_token': access_token, 'refresh_token': refresh_token})
        return response
    else:
       raise HTTPException(status_code=401, detail="Wrong login details!")


@router.post('/refresh')
def refresh_token(data: RefreshRequest) -> JSONResponse:
    refresh_token = data.refresh_token
    if decodeJWT(refresh_token):
        access_token = signJWT(data.user_id, 30)
        return JSONResponse(content={'access_token': access_token})
    else:
        auth_service.delete_refresh_from_db(data.user_id)  
        return JSONResponse(content={'access_token': None})   
    
@router.post('/logout')
def logout(data: LogoutRequest) -> None:
    auth_service.delete_refresh_from_db(data.user_id)
    