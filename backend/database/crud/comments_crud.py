from datetime import datetime
from backend.database.session_decorator import Sessioner
from backend.database.models import Comments
from sqlalchemy import desc



class CommentsCrud():
    @Sessioner.dbconnect
    def create_comment(self, data, session):
        comment = Comments(CreatorCommentID=data.user_id,
                           PostParentID=data.post_id,
                           text=data.comment_text,
                           time=datetime.now()
                           )
        session.add(comment)
        return session.query(Comments).filter(Comments.CreatorCommentID==data.user_id,
                                              Comments.PostParentID==data.post_id,
                                              Comments.text==data.comment_text).first().CommentID

    @Sessioner.dbconnect
    def get_comment_info_by_id(self, comment_id, session):
            result = session.query(Comments).get(comment_id)
            return {'comment_id': result.CommentID,
                    'creator_id': result.CreatorCommentID,
                    'comment_text': result.text,
                    'comment_time': result.time}

    @Sessioner.dbconnect
    def get_comments_by_postid(self, post_id, session):
        result = [{'comment_id': comment.CommentID,
                    'creator_id': comment.CreatorCommentID,
                    'comment_text': comment.text,
                    'comment_time': comment.time} 
                    for comment in
                    session.query(Comments).filter(Comments.PostParentID==post_id).order_by(desc(Comments.time)).all()]
        return result

    @Sessioner.dbconnect
    def get_comment_count_by_postid(self, post_id, session):
        return session.query(Comments).filter(Comments.PostParentID==post_id).count()
    
    @Sessioner.dbconnect
    def get_comments_id_to_delete(self, post_id, session):
        query = session.query(Comments).filter(Comments.PostParentID==post_id).all()
        comments_deleted_id = [comment.CommentID for comment in query]
        return comments_deleted_id

    @Sessioner.dbconnect
    def update_comment(self, data, session):
        session.query(Comments).filter(Comments.CommentID==data.comment_id, Comments.CreatorCommentID==data.user_id).update({Comments.text: data.new_text})

    @Sessioner.dbconnect
    def delete_comment(self, data, session):
        session.delete(session.query(Comments).filter(Comments.CommentID==data.comment_id).first())
    
    @Sessioner.dbconnect
    def delete_all_comments_by_postid(self, post_id, session):
        session.query(Comments).filter(Comments.PostParentID==post_id).delete()