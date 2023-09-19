from backend.database.crud.user_crud import UserCrud
from backend.database.crud.subscriptions_crud import SubscriptionsCrud
from backend.logic.dtos.requests.subscriptions.follow_unfollow_request import FollowUnfollowRequest

u_c = UserCrud()
s_c = SubscriptionsCrud()


class SubscriptionsService():
    def subscribe_unsubscribe(self, data: FollowUnfollowRequest) -> bool:
        if s_c.get_subscription_existence(data):
            s_c.delete_subscription(data)
        else:
            s_c.create_subscription(data)
    
    def is_followed(self, data: FollowUnfollowRequest) -> bool:
        return s_c.get_subscription_existence(data)
    
    def get_subscribers(self, user_id: int) -> dict:
        result = dict()
        subscribers_id = s_c.get_subscribers(user_id)
        for id in subscribers_id:
            result[id] = u_c.get_login_by_id(id)
        return result
    
    def get_subscriptions(self, user_id: int) -> dict:
        result = dict()
        subscriptions_id = s_c.get_subscriptions(user_id)
        for id in subscriptions_id:
            result[id] = u_c.get_login_by_id(id)
        return result