from backend.database.session_decorator import Sessioner 
from backend.database.models import RatingPosts
from backend.domain.exception import ValidationError



class PostsRatingCrud():
    @Sessioner.dbconnect
    def create_post_rating(self, rate_info, session):

        rating = RatingPosts(RatedID=rate_info.user_id, RatingReceiverID=rate_info.rating_receiver,
                            RatedPostID=rate_info.post_id, Value=rate_info.rating_value
                            )
        session.add(rating)

    @Sessioner.dbconnect
    def get_rating_value(self, post_id, user_id, session):
        query = session.query(RatingPosts).filter(RatingPosts.RatedID==user_id,
                                             RatingPosts.RatedPostID==post_id,
                                                )
        return query.first().Value
        
    @Sessioner.dbconnect
    def get_user_posts_rating_by_id(self, user_id, session):
        query = [i.Value for i in 
                        session.query(RatingPosts).filter(RatingPosts.RatingReceiverID==user_id)
                        ]
        return sum(query) if query != [] else 0

    @Sessioner.dbconnect
    def get_post_rating_by_postid(self, post_id, session):
        query = [i.Value for i in 
                        session.query(RatingPosts).filter(RatingPosts.RatedPostID==post_id)
                        ]
        if query != []:
            return sum(query)
        else:
            return 0

    @Sessioner.dbconnect
    def rate_existence(self, rate_info, session):
        if session.query(RatingPosts).filter(
                                        RatingPosts.RatedID==rate_info.user_id,
                                        RatingPosts.RatedPostID==rate_info.post_id).first():
            return True
        else:
            return False
    
    @Sessioner.dbconnect
    def rate_existence_by_value(self, rate_info, session):
        if session.query(RatingPosts).filter(
                                        RatingPosts.RatedID==rate_info.user_id,
                                        RatingPosts.RatedPostID==rate_info.post_id,
                                        RatingPosts.Value==rate_info.rating_value).first():
            return True
        else:
            return False
        
    @Sessioner.dbconnect
    def check_rating_existence(self, post_id, user_id, session):
        query = session.query(RatingPosts).filter(RatingPosts.RatedID==user_id,
                                             RatingPosts.RatedPostID==post_id
                                                )
        if query.first():
            return True
        else:
            return False
        
    @Sessioner.dbconnect
    def delete_rating(self, rate_info, session):
        rating_to_delete = session.query(RatingPosts).filter(RatingPosts.RatedID == rate_info.user_id,
                                                             RatingPosts.RatedPostID == rate_info.post_id
                                                                ).first()
        session.delete(rating_to_delete)

    @Sessioner.dbconnect
    def delete_all_ratings_by_post_id(self, post_id, session):
        session.query(RatingPosts).filter(RatingPosts.RatedPostID==post_id).delete()