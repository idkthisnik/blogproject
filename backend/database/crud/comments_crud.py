from typing import List
from sqlalchemy import desc
from datetime import datetime

from database.models import Comments
from database.session_decorator import Sessioner
from logic.dtos.requests.comment.createcomment_request import CreateCommentRequest
from logic.dtos.requests.comment.updatecomment_request import UpdateCommentRequest
from logic.dtos.requests.comment.deletecomment_request import DeleteCommentRequest



class CommentsCrud():
    @Sessioner.dbconnect
    def create_comment(self, data: CreateCommentRequest, session) -> int:
        comment = Comments(
            CreatorCommentID=data.user_id, PostParentID=data.post_id,
            text=data.comment_text, time=datetime.now()
        )
        
        session.add(comment)
        
        result = session.query(Comments).filter(
            Comments.CreatorCommentID==data.user_id,
            Comments.PostParentID==data.post_id,
            Comments.text==data.comment_text
        ).first().CommentID
        
        return result

    @Sessioner.dbconnect
    def get_comment(self, comment_id: int, session) -> dict:
        result = session.query(Comments).get(comment_id)
        return {
            'comment_id': result.CommentID,
            'creator_id': result.CreatorCommentID,
            'comment_text': result.text,
            'comment_time': result.time
        }

    @Sessioner.dbconnect
    def get_comments_for_post(self, post_id: int, session) -> List[dict]:
        result = [{
            'comment_id': comment.CommentID,
            'creator_id': comment.CreatorCommentID,
            'comment_text': comment.text,
            'comment_time': comment.time
          } 
        for comment
        in session.query(Comments)\
            .filter(Comments.PostParentID==post_id)\
            .order_by(desc(Comments.time))\
            .all()]
        
        return result

    @Sessioner.dbconnect
    def get_comments_count_for_post(self, post_id: int, session) -> int:
        result = session.query(Comments)\
                        .filter(Comments.PostParentID==post_id)\
                        .count()
        return result
                    
    @Sessioner.dbconnect
    def get_comments_ids_to_delete(self, post_id: int, session) -> List[int]:
        query = session.query(Comments)\
                        .filter(Comments.PostParentID==post_id)\
                        .all()
        comments_deleted_id = [comment.CommentID for comment in query]
        return comments_deleted_id

    @Sessioner.dbconnect
    def update_comment(self, data: UpdateCommentRequest, session) -> None:
        session.query(Comments)\
               .filter(
                   Comments.CommentID==data.comment_id,
                   Comments.CreatorCommentID==data.user_id
                )\
               .update({Comments.text: data.new_text})

    @Sessioner.dbconnect
    def delete_comment(self, data: DeleteCommentRequest, session) -> None:
        session.delete(
            session.query(Comments)\
                   .filter(Comments.CommentID==data.comment_id)\
                   .first()
        )
    
    @Sessioner.dbconnect
    def delete_all_comments_for_post(self, post_id: int, session) -> None:
        session.query(Comments)\
               .filter(Comments.PostParentID==post_id)\
               .delete()