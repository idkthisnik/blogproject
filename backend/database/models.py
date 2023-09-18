from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .connection import Base


class Users(Base): 
    __tablename__ = 'Users'
    
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    email = Column(String)
    refresh = Column(String(200))
    salt = Column(String(200))
    post = relationship('Posts')
    comment = relationship('Comments')
    
    
    def __init__(self, login, password, email, refresh, salt):
        self.login = login
        self.password = password
        self.email = email
        self.refresh = refresh
        self.salt = salt


class Posts(Base):
    __tablename__ = 'Posts'
    
    PostID = Column(Integer, primary_key=True, autoincrement=True)
    CreatorPostID = Column(Integer, ForeignKey('Users.UserID'))
    text = Column(String(2000))
    time = Column(String(32))
    coment = relationship('Comments')
    rate = relationship('RatingPosts')
    

class RatingPosts(Base):
    __tablename__ = 'RatingPosts'
    
    RatingID = Column(Integer, primary_key=True, autoincrement=True)
    RatedID = Column(Integer, ForeignKey('Users.UserID'))
    RatingReceiverID = Column(Integer, ForeignKey('Users.UserID'))
    RatedPostID = Column(Integer, ForeignKey('Posts.PostID'))
    Value = Column(Integer)
    
    rated_id = relationship("Users", foreign_keys=[RatedID])
    rating_receiver = relationship("Users", foreign_keys=[RatingReceiverID])
    

class RatingComments(Base):
    __tablename__ = 'RatingComments'
    
    RatingID = Column(Integer, primary_key=True, autoincrement=True)
    RatedID = Column(Integer, ForeignKey('Users.UserID'))
    RatingReceiverID = Column(Integer, ForeignKey('Users.UserID'))
    RatedCommentID = Column(Integer, ForeignKey('Comments.CommentID'))
    Value = Column(Integer)
    
    rated_id = relationship("Users", foreign_keys=[RatedID])
    rating_receiver = relationship("Users", foreign_keys=[RatingReceiverID])


class Subscriptions(Base):
    __tablename__ = 'Subscriptions'
    
    SubscriptionID = Column(Integer, primary_key=True, autoincrement=True)
    
    AccountID = Column(Integer, ForeignKey('Users.UserID'))
    SubscriberID = Column(Integer, ForeignKey('Users.UserID'))
    
    AccountID_relation = relationship('Users', foreign_keys=[AccountID])
    SubscriberID_relation = relationship('Users', foreign_keys=[SubscriberID])

    

class Comments(Base):
    __tablename__ = 'Comments'
    
    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    CreatorCommentID = Column(Integer, ForeignKey('Users.UserID'))
    PostParentID = Column(Integer, ForeignKey('Posts.PostID'))
    text = Column(String(2000))
    time = Column(String(32))
    rate = relationship('RatingComments')