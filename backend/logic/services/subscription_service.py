from backend.database.crud.subscriptions_crud import SubscriptionsCrud
from backend.database.crud.user_crud import UserCrud

users_crud = UserCrud()
subscriptions_crud = SubscriptionsCrud()


class SubscriptionsService():
    def subscribe_unsubscribe(self, data):
        if subscriptions_crud.get_subscriptions_existence(data):
            subscriptions_crud.delete_subscription(data)
        else:
            subscriptions_crud.create_subscription(data)
    
    def is_followed(self, data):
        return subscriptions_crud.get_subscriptions_existence(data)
    
    
    
    def get_subscribers(self, user_id):
        result = dict()
        subscribers_id = subscriptions_crud.get_subscriber_list(user_id)
        for id in subscribers_id:
            result[id] = users_crud.get_login_by_id(id)
        return result
    
    
    def get_subscriptions(self, user_id):
        result = dict()
        subscriptions_id = subscriptions_crud.get_subscriptions_list(user_id)
        for id in subscriptions_id:
            result[id] = users_crud.get_login_by_id(id)
        return result