from backend.database.crud.user_crud import UserCrud
from backend.logic.dtos.responses.auth.registration_request import RegistrationRequestToDB, LoginRequestToDB
from .hash_service import HashService

hash_service = HashService()
user_crud = UserCrud()

class AuthService():
    def registr_user(self, info):
        if user_crud.check_user_in_db(info.username):
            return None
        else:
            salt = hash_service.generate_salt()
            hashed_password = hash_service.password_hasher(info.entered_password, salt)
            updated_info = RegistrationRequestToDB(username=info.username,
                                                    password=hashed_password,
                                                    email=info.email,
                                                    salt=salt.decode()
            )
            return user_crud.create_user(updated_info)
    
    def check_user(self, info):
        user_salt = user_crud.get_salt(info.username)
        if user_salt:
            user_salt = user_salt.encode()
            hashed_password = hash_service.password_hasher(info.entered_password, user_salt)
            updated_info = LoginRequestToDB(username=info.username,
                                                    password=hashed_password)
            return user_crud.check_user(updated_info)
        else:
            return False
    
    def get_userId(self, login):
        return user_crud.get_user_id_by_login(login)
     
    def add_refresh_to_db(self, user_id, refresh):
        return user_crud.add_refresh(user_id, refresh) 
    
    def delete_refresh_from_db(self, user_id):
        return user_crud.delete_refresh(user_id)