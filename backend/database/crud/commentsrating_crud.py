from backend.domain.exception import ValidationError
from backend.database.session_decorator import Sessioner
from backend.database.models import RatingComments



class CommentsRatingCrud():
    @Sessioner.dbconnect
    def create_comment_rating(self, rate_info, session):
        rating = RatingComments(RatedID=rate_info.user_id, RatingReceiverID=rate_info.rating_receiver,
                                RatedCommentID=rate_info.comment_id, Value=rate_info.rating_value)
        session.add(rating)
        
    @Sessioner.dbconnect
    def get_user_comments_rating_by_id(self, user_id, session):
        query = [i.Value for i in 
                        session.query(RatingComments).filter(RatingComments.RatingReceiverID==user_id)
                        ]
        return sum(query) if query != [] else 0
    
    @Sessioner.dbconnect
    def get_comment_rating_by_comment_id(self, comment_id, session):
        results = session.query(RatingComments).filter(RatingComments.RatedCommentID==comment_id).all()
        total_rating = sum(rating.Value for rating in results)
        return total_rating
    
    @Sessioner.dbconnect
    def get_rating_value(self, comment_id, user_id, session):
        return session.query(RatingComments).filter(RatingComments.RatedID==user_id,
                                                    RatingComments.RatedCommentID==comment_id
                                                ).first().Value
     
    @Sessioner.dbconnect
    def check_rating_existence(self, rate_info, session):
        query = session.query(RatingComments).filter(RatingComments.RatedID==rate_info.user_id,
                                             RatingComments.RatedCommentID==rate_info.comment_id
                                                )
        if query.first():
            return True
        else:
            return False
    
    @Sessioner.dbconnect
    def rate_existence_by_value(self, rate_info, session):
        if session.query(RatingComments).filter(
                                        RatingComments.RatedID==rate_info.user_id,
                                        RatingComments.RatedCommentID==rate_info.comment_id,
                                        RatingComments.Value==rate_info.rating_value).first():
            return True
        else:
            return False

    @Sessioner.dbconnect
    def delete_rating(self, rate_info, session):
        query = session.query(RatingComments).filter(RatingComments.RatedID==rate_info.user_id,
                                                     RatingComments.RatedCommentID==rate_info.comment_id).first()
        session.delete(query)
        
    @Sessioner.dbconnect
    def delete_comment_rating_by_commentid(self, comment_id, session):
        session.query(RatingComments).filter(RatingComments.RatedCommentID==comment_id).delete()