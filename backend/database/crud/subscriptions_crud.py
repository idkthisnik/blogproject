from backend.database.session_decorator import Sessioner
from backend.database.models import Subscriptions


class SubscriptionsCrud():
    @Sessioner.dbconnect
    def create_subscription(self, data, session):
        subscribe = Subscriptions(AccountID=data.user_id,
                                  SubscriberID=data.subscriber_id
                                  )
        session.add(subscribe)

    @Sessioner.dbconnect
    def get_subscriber_list(self, user_id, session):
        result = [user.SubscriberID for user in session.query(Subscriptions).filter(
                                                 Subscriptions.AccountID==user_id
                                                 ).all()
        ]
        return result
    
    @Sessioner.dbconnect
    def get_subscriptions_list(self, user_id, session):
        result = [user.AccountID for user in session.query(Subscriptions).filter(
                                                 Subscriptions.SubscriberID==user_id
                                                 ).all()
        ]
        return result 
       
    @Sessioner.dbconnect
    def get_subscriptions_existence(self, data, session):
        if session.query(Subscriptions).filter(Subscriptions.AccountID==data.user_id,
                                               Subscriptions.SubscriberID==data.subscriber_id
                                               ).first():
            return True
        else:
            return False

    @Sessioner.dbconnect
    def get_subscriptions_count(self, user_id, session):
            return session.query(Subscriptions).filter(
                                                Subscriptions.SubscriberID==user_id
                                                ).count()
            
    @Sessioner.dbconnect
    def get_subscribers_count(self, user_id, session):
            return session.query(Subscriptions).filter(
                                                Subscriptions.AccountID==user_id
                                                ).count()        

    @Sessioner.dbconnect
    def delete_subscription(self, data, session):
        subscribe_to_delete = session.query(Subscriptions).filter(
                            Subscriptions.AccountID==data.user_id,
                            Subscriptions.SubscriberID==data.subscriber_id
                            ).first()
        session.delete(subscribe_to_delete)