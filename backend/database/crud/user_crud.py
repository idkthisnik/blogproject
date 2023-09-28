from typing import List

from database.models import Users
from database.session_decorator import Sessioner
from logic.dtos.requests.settings.updatelogin_request import UpdateLoginRequest
from logic.dtos.requests.settings.updateemail_request import UpdateEmailRequest
from logic.dtos.requests.settings.deleteaccount_request import DeleteProfileRequest
from logic.dtos.requests.settings.updatepassword_request import UpdatePasswordRequestToDB
from logic.dtos.requests.auth.auth_request import LoginRequestToDB, RegistrationRequestToDB

   

class LoginPasswordVerify():
    @Sessioner.dbconnect
    def login_password_verify(self, data, session) -> bool:
        query = session.query(Users).filter(Users.login==data.login, Users.password==data.password).first()
        return True if query else False


class UserCrud():
    ####Global user crud####
    @Sessioner.dbconnect
    def auth_user(self, data: LoginRequestToDB, session) -> bool:
        query = session.query(Users).filter(
                                        Users.login==data.username,
                                        Users.password==data.password
                                   ).first()
        return True if query else False

    @Sessioner.dbconnect
    def delete_user(self, data: DeleteProfileRequest, session) -> None:
        user_to_delete = session.query(Users).filter(Users.login==data.login).first()
        session.delete(user_to_delete)
        
    ####Login and ID crud####
    @Sessioner.dbconnect
    def create_user(self, data: RegistrationRequestToDB, session) -> int:
        session.add(
            Users(
                login=data.username,
                password=data.password,
                email=data.email,
                salt=data.salt,
                refresh=None,
                profile_image="default.png"
            )
        )
        return session.query(Users).filter(Users.login==data.username).first().UserID
    
    @Sessioner.dbconnect
    def check_user_existence(self, login: str, session) -> bool:   
        query = session.query(Users).filter(Users.login==login).first()
        return True if query else False
    
    @Sessioner.dbconnect
    def get_all_users(self, session) -> List[dict]:    
        result = []
        for user in session.query(Users).all():
            result.append({
                'user_id': user.UserID,
                'login': user.login
            })
        return result if result else None
        
    @Sessioner.dbconnect
    def get_user_by_id(self, user_id: int, session) -> dict:    
        user = session.query(Users).get(user_id)
        return {
            'login': user.login,
            'email': user.email
        } if user else None

    @Sessioner.dbconnect
    def get_login_by_id(self, user_id: int, session) -> str:
        return session.query(Users).get(user_id).login
    
    @Sessioner.dbconnect
    def get_user_id_by_login(self, login: str, session) -> int:
        return session.query(Users).filter(Users.login==login).first().UserID
    
    @Sessioner.dbconnect
    def update_login(self, data: UpdateLoginRequest, session) -> None:
        session.query(Users).filter(
                                Users.login==data.login
                           ).update(
                               {Users.login: data.new_login}
        )
            
    @Sessioner.dbconnect
    def update_password(self, data: UpdatePasswordRequestToDB, session) -> None:
        session.query(Users).filter(
                                Users.login==data.login
                            ).update(
                                {Users.password: data.new_password}
        )

    @Sessioner.dbconnect
    def update_email(self, data: UpdateEmailRequest, session) -> None:
        session.query(Users).filter(
                                Users.login==data.login
                           ).update(
                               {Users.email: data.new_email}
        )
    
    ####Salt crud####
    @Sessioner.dbconnect
    def add_salt(self, user_id: int, salt: str, session) -> None:
        session.query(Users).filter(
                                Users.UserID==user_id
                           ).update(
                                {Users.salt: salt}
        )
        
    @Sessioner.dbconnect
    def get_salt(self, username: str, session) -> str:
        query = session.query(Users).filter(Users.login==username).first()
        return query.salt if query else None
    
    ####Refresh crud####
    @Sessioner.dbconnect
    def add_refresh(self, user_id: int, refresh: str, session):
        session.query(Users).filter(
                                Users.UserID==user_id
                           ).update(
                               {Users.refresh: refresh}
        )   
        
    @Sessioner.dbconnect
    def delete_refresh(self, user_id: int, session):
        session.query(Users).filter(
                                Users.UserID==user_id
                           ).update(
                               {Users.refresh: None}
        )
                           
    ####Profile page crud####
    @Sessioner.dbconnect
    def get_current_profile_image(self, user_id: int, session) -> str:
        return session.query(Users).filter(Users.UserID==user_id).first().profile_image
    
    @Sessioner.dbconnect
    def set_new_profile_image(self, data, session) -> None:
        session.query(Users).filter(
                                Users.UserID==data.user_id
                           ).update(
                               {Users.profile_image: data.profile_image}
        )