from .hash_service import HashService
from backend.logic.dtos.requests.settings.updatelogin_request import UpdateLoginRequest
from backend.logic.dtos.requests.settings.updateemail_request import UpdateEmailRequest
from backend.logic.dtos.requests.settings.deleteaccount_request import DeleteProfileRequest
from backend.database.crud.user_crud import (
    UserCrud,
    LoginPasswordVerify
)
from backend.logic.dtos.requests.settings.updatepassword_request import (
    UpdatePasswordRequestToDB,
    UpdatePasswordRequest
)


users_crud = UserCrud()
login_password_verify = LoginPasswordVerify()
hash_service = HashService()


class SettingsService():
    def update_login(self, data: UpdateLoginRequest) -> bool | None:
        salt = users_crud.get_salt(data.login)
        if salt:
            salt = salt.encode()
            hashed_password = hash_service.password_hasher(data.password, salt)
            updated_info = UpdateLoginRequest(
                login=data.login,
                password=hashed_password,
                new_login=data.new_login
            )
            
            if login_password_verify.login_password_verify(updated_info):
                users_crud.update_login(updated_info)
                return True
            else:
                return None
        else:
            return None
    
    def update_password(self, data: UpdatePasswordRequest) -> bool | None:
        salt = users_crud.get_salt(data.login)
        if salt:
            salt = salt.encode()
            new_salt = hash_service.generate_salt()
            
            hashed_password = hash_service.password_hasher(data.password, salt)
            new_hashed_password = hash_service.password_hasher(data.new_password, new_salt)
            
            updated_info = UpdatePasswordRequestToDB(
                login=data.login,
                password=hashed_password,
                new_password=new_hashed_password
            )
            
            if login_password_verify.login_password_verify(updated_info):
                user_id = users_crud.get_user_id_by_login(data.login)
                users_crud.update_password(updated_info)
                users_crud.add_salt(user_id, new_salt.decode())
                return True
            else:
                return None
        else:
            return None
        
    def update_email(self, data: UpdateEmailRequest) -> bool | None:
        salt = users_crud.get_salt(data.login)
        if salt:
            salt = salt.encode()
            hashed_password = hash_service.password_hasher(data.password, salt)
            
            updated_info = UpdateEmailRequest(
                login=data.login,
                password=hashed_password,
                new_email=data.new_email
            )
            
            if login_password_verify.login_password_verify(updated_info):
                users_crud.update_email(updated_info)
                return True
            else:
                return None
        else: 
            return None
    
    def delete_account(self, data: DeleteProfileRequest) -> bool | None:
        salt = users_crud.get_salt(data.login)
        if salt:
            salt = salt.encode()
            hashed_password = hash_service.password_hasher(data.password, salt)
            
            updated_info = DeleteProfileRequest(
                login=data.login,
                password=hashed_password,
            )
            
            if login_password_verify.login_password_verify(updated_info):
                users_crud.delete_user(updated_info)
                return True
            else:
                return None
        else: 
            return None