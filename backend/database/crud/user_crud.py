from backend.database.session_decorator import Sessioner
from backend.domain.exception import ValidationError
from backend.database.models import Users

   
class LoginPasswordVerify():
    @Sessioner.dbconnect
    def login_password_verify(self, data, session):
        if session.query(Users).filter(Users.login==data.login, Users.password==data.password).first():
            return True
        else:
            return False 


class UserCrud():
    ####Global user crud####
    @Sessioner.dbconnect
    def check_user(self, data, session):
        if session.query(Users).filter(Users.login==data.username, Users.password==data.password).first():
            return True
        return False

    @Sessioner.dbconnect
    def delete_user(self, data, session):
        user_to_delete = session.query(Users).filter(Users.login==data.login).first()
        session.delete(user_to_delete)
        
    ####Login and Id crud####
    @Sessioner.dbconnect
    def create_user(self, data, session):
        session.add(Users(login=data.username, password=data.password, email=data.email, salt=data.salt, refresh=None))
        return session.query(Users).filter(Users.login==data.username).first().UserID
    
    @Sessioner.dbconnect
    def check_user_in_db(self, login, session):   
        return session.query(Users).filter(Users.login==login).first()
    
    @Sessioner.dbconnect
    def get_all_users(self, session):    
        result = []
        users = session.query(Users).all()
        for user in users:
            result.append({'user_id': user.UserID, 'login': user.login})
        return result if result else None
        
    @Sessioner.dbconnect
    def get_user_by_id(self, user_id, session):    
        user = session.query(Users).get(user_id)
        return {'login': user.login, 'email': user.email} if user else None

    @Sessioner.dbconnect
    def get_login_by_id(self, user_id, session):
        return session.query(Users).get(user_id).login
    
    @Sessioner.dbconnect
    def get_user_id_by_login(self, login, session):
        return session.query(Users).filter(Users.login==login).first().UserID
    
    @Sessioner.dbconnect
    def update_login(self, data, session):
        session.query(Users).filter(Users.login==data.login).update({Users.login: data.new_login})
            
    @Sessioner.dbconnect
    def update_password(self, data, session):
            session.query(Users).filter(Users.login==data.login).update({Users.password: data.new_password})

    @Sessioner.dbconnect
    def update_email(self, data, session):
        session.query(Users).filter(Users.login==data.login).update({Users.email: data.new_email})
    
    ####Salt crud####
    @Sessioner.dbconnect
    def add_salt(self, user_id, salt, session):
        session.query(Users).filter(Users.UserID==user_id).update({Users.salt: salt})
        
    @Sessioner.dbconnect
    def get_salt(self, username, session):
        query = session.query(Users).filter(Users.login==username).first()
        return query.salt if query else None
    
    ####Refresh crud####
    @Sessioner.dbconnect
    def add_refresh(self, user_id, refresh, session):
        session.query(Users).filter(Users.UserID==user_id).update({Users.refresh: refresh})   
        
    @Sessioner.dbconnect
    def delete_refresh(self, user_id, session):
        session.query(Users).filter(Users.UserID==user_id).update({Users.refresh: None})      