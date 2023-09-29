from database.models import RatingPosts
from database.session_decorator import Sessioner 
from logic.dtos.requests.rating.ratepost_request import RatePostRequest



class PostsRatingCrud():
    @Sessioner.dbconnect
    def create_post_rating(self, rate_info: RatePostRequest, session) -> None:
        rating = RatingPosts(
            RatedID=rate_info.user_id,
            RatingReceiverID=rate_info.rating_receiver,
            RatedPostID=rate_info.post_id,
            Value=rate_info.rating_value
        )
        session.add(rating)

    @Sessioner.dbconnect
    def get_post_rating_value(self, post_id: int, user_id: int, session) -> int:
        return session.query(RatingPosts)\
                      .filter(
                          RatingPosts.RatedID==user_id,
                          RatingPosts.RatedPostID==post_id,
                       )\
                      .first()\
                      .Value
        
    @Sessioner.dbconnect
    def get_user_total_posts_rating(self, user_id: int, session) -> int:
        values_list = [
            i.Value 
            for i 
            in session.query(RatingPosts)\
                      .filter(RatingPosts.RatingReceiverID==user_id)
        ]
        return values_list

    @Sessioner.dbconnect
    def get_post_total_rating(self, post_id: int, session) -> int:
        results = session.query(RatingPosts)\
                         .filter(RatingPosts.RatedPostID==post_id)\
                         .all()
        total_rating = [rating.Value for rating in results]
        
        return total_rating

    @Sessioner.dbconnect
    def check_post_rating_by_value(
        self,
        rate_info: RatePostRequest,
        session
    ) -> bool:
        
        if session.query(RatingPosts)\
                  .filter(
                      RatingPosts.RatedID==rate_info.user_id,
                      RatingPosts.RatedPostID==rate_info.post_id,
                      RatingPosts.Value==rate_info.rating_value
                   )\
                  .first():
            return True
        else:
            return False
        
    @Sessioner.dbconnect
    def check_post_rating_existence(
        self,
        post_id: int,
        user_id: int,
        session
    ) -> bool:
        
        query = session.query(RatingPosts)\
                       .filter(
                           RatingPosts.RatedID==user_id,
                           RatingPosts.RatedPostID==post_id
                        )
        return True if query.first() else False
        
    @Sessioner.dbconnect
    def delete_post_rating(self, rate_info: RatePostRequest, session) -> None:
        rating_to_delete = session.query(RatingPosts)\
                                  .filter(
                                      RatingPosts.RatedID == rate_info.user_id,
                                      RatingPosts.RatedPostID == rate_info.post_id
                                   )\
                                  .first()
                                  
        session.delete(rating_to_delete)

    @Sessioner.dbconnect
    def delete_all_post_rating(self, post_id: int, session) -> None:
        session.query(RatingPosts)\
               .filter(RatingPosts.RatedPostID==post_id)\
               .delete()