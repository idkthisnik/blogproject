from .hash_service import HashService
from database.crud.user_crud import UserCrud
from logic.dtos.requests.auth.auth_request import (
    RegistrationRequestToDB,
    LoginRequestToDB,
    RegistrationRequest,
    LoginRequest
)


h_s = HashService()
u_c = UserCrud()

class AuthService():
    def registr_user(self, info: RegistrationRequest) -> int:
        if u_c.check_user_existence(info.username):
            return None
        else:
            salt = h_s.generate_salt()
            
            hashed_password = h_s.password_hasher(
                info.entered_password,
                salt
            )
            
            updated_info = RegistrationRequestToDB(
                username=info.username,
                password=hashed_password,
                email=info.email,
                salt=salt.decode()
            )
            return u_c.create_user(updated_info)
    
    def check_user(self, info: LoginRequest) -> bool:
        user_salt = u_c.get_salt(info.username)
        if user_salt:
            user_salt = user_salt.encode()
            
            hashed_password = h_s.password_hasher(
                info.entered_password,
                user_salt
            )
            
            updated_info = LoginRequestToDB(
                username=info.username,
                password=hashed_password
                )
            return u_c.auth_user(updated_info)
        else:
            return False
    
    def get_user_id(self, login: str) -> int:
        return u_c.get_user_id_by_login(login)
     
    def add_refresh_to_db(self, user_id: int, refresh: str) -> None:
        return u_c.add_refresh(user_id, refresh) 
    
    def delete_refresh_from_db(self, user_id: int) -> None:
        return u_c.delete_refresh(user_id)