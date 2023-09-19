from backend.database.models import RatingComments
from backend.database.session_decorator import Sessioner
from backend.logic.dtos.requests.rating.ratecomment_request import RateCommentRequest



class CommentsRatingCrud():
    @Sessioner.dbconnect
    def create_comment_rating(self, rate_info: RateCommentRequest, session) -> None:
        rating = RatingComments(
            RatedID=rate_info.user_id,
            RatingReceiverID=rate_info.rating_receiver,
            RatedCommentID=rate_info.comment_id,
            Value=rate_info.rating_value
        )
        session.add(rating)
        
    @Sessioner.dbconnect
    def get_user_total_comments_rating(self, user_id: int, session) -> int:
        query = [i.Value 
                 for i 
                 in session.query(RatingComments).filter(RatingComments.RatingReceiverID==user_id)
        ]
        return sum(query) if query != [] else 0
    
    @Sessioner.dbconnect
    def get_comment_total_rating(self, comment_id: int, session) -> int:
        results = session.query(RatingComments).filter(
                                                   RatingComments.RatedCommentID==comment_id
                                              ).all()
        total_rating = sum(rating.Value for rating in results)
        return total_rating
    
    @Sessioner.dbconnect
    def get_comment_rating_value(self, comment_id: int, user_id: int, session) -> int:
        return session.query(RatingComments).filter(
                                                RatingComments.RatedID==user_id,
                                                RatingComments.RatedCommentID==comment_id
                                           ).first().Value
     
    @Sessioner.dbconnect
    def check_comment_rating_existence(self, rate_info: RateCommentRequest, session) -> bool:
        query = session.query(RatingComments).filter(
                                                 RatingComments.RatedID==rate_info.user_id,
                                                 RatingComments.RatedCommentID==rate_info.comment_id
        )
        return True if query.first() else False

    @Sessioner.dbconnect
    def check_comment_rating_by_value(self, rate_info: RateCommentRequest, session) -> bool:
        if session.query(RatingComments).filter(
                                            RatingComments.RatedID==rate_info.user_id,
                                            RatingComments.RatedCommentID==rate_info.comment_id,
                                            RatingComments.Value==rate_info.rating_value
                                       ).first():
            return True
        else:
            return False

    @Sessioner.dbconnect
    def delete_comment_rating(self, rate_info: RateCommentRequest, session) -> None:
        session.query(RatingComments).filter(
                                         RatingComments.RatedID==rate_info.user_id,
                                         RatingComments.RatedCommentID==rate_info.comment_id
                                    ).delete()