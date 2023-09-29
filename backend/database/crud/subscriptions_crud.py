from typing import List

from database.models import Subscriptions
from database.session_decorator import Sessioner
from logic.dtos.requests.subscriptions.follow_unfollow_request import FollowUnfollowRequest



class SubscriptionsCrud():
    @Sessioner.dbconnect
    def create_subscription(self, data: FollowUnfollowRequest, session) -> None:
        subscribe = Subscriptions(
            AccountID=data.user_id,
            SubscriberID=data.subscriber_id
        )
        session.add(subscribe)

    @Sessioner.dbconnect
    def get_subscribers(self, user_id: int, session) -> List[int]:
        result = [
            user.SubscriberID 
            for user
            in session.query(Subscriptions)\
                      .filter(Subscriptions.AccountID==user_id)\
                      .all()
        ]
        return result
    
    @Sessioner.dbconnect
    def get_subscriptions(self, user_id: int, session) -> List[int]:
        result = [
            user.AccountID
            for user
            in session.query(Subscriptions)\
                      .filter(Subscriptions.SubscriberID==user_id)\
                      .all()
        ]
        return result 
       
    @Sessioner.dbconnect
    def get_subscription_existence(
        self,
        data: FollowUnfollowRequest,
        session
    ) -> bool:
        
        query = session.query(Subscriptions)\
                       .filter(
                           Subscriptions.AccountID==data.user_id,
                           Subscriptions.SubscriberID==data.subscriber_id
                        )\
                       .first()
        return True if query else False

    @Sessioner.dbconnect
    def get_subscriptions_count(self, user_id: int, session) -> int:
        return session.query(Subscriptions)\
                      .filter(Subscriptions.SubscriberID==user_id)\
                      .count()
            
    @Sessioner.dbconnect
    def get_subscribers_count(self, user_id: int, session) -> int:
        return session.query(Subscriptions)\
                      .filter(Subscriptions.AccountID==user_id)\
                      .count()        

    @Sessioner.dbconnect
    def delete_subscription(self, data: FollowUnfollowRequest, session) -> None:
        subscribe_to_delete = session.query(
            Subscriptions
        )\
        .filter(
            Subscriptions.AccountID==data.user_id,
            Subscriptions.SubscriberID==data.subscriber_id
        )\
        .first()
        
        session.delete(subscribe_to_delete)