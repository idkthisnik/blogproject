from sqlalchemy import desc
from datetime import datetime

from database.models import Posts
from database.session_decorator import Sessioner
from logic.dtos.requests.post.createpost_request import CreatePostRequest
from logic.dtos.requests.post.updatepost_request import UpdatePostRequest



class PostsCrud():
    @Sessioner.dbconnect
    def create_post(self, data: CreatePostRequest, session) -> int:
        post = Posts(
            CreatorPostID=data.user_id,
            text=data.post_text,
            time=datetime.now()
        )
        session.add(post)
        return session.query(Posts)\
                      .filter(
                           Posts.CreatorPostID==data.user_id,
                           Posts.text==data.post_text
                       )\
                      .first()\
                      .PostID
        
    @Sessioner.dbconnect
    def get_post(self, post_id: int, session) -> dict | None:
        data = session.query(Posts)\
                      .filter(Posts.PostID==post_id)\
                      .first()
        if data:
            result = {
                'post_id': data.PostID,
                'post_creator_id': data.CreatorPostID,
                'post_text': data.text,
                'post_time': data.time
            }      
            return result
        else:
            return None

    @Sessioner.dbconnect
    def get_all_posts(self, sorted: int, session) -> dict | None:
        if sorted:
            posts = session.query(Posts)\
                           .filter(Posts.CreatorPostID==sorted)\
                           .order_by(desc(Posts.time))\
                           .all()
        else:
            posts = session.query(Posts).order_by(desc(Posts.time)).all()
        if posts:
            result = [{
                'post_id': post.PostID,
                'post_creator_id': post.CreatorPostID,
                'post_text': post.text,
                'post_time': post.time.split('.')[0]
              }
            for post 
            in posts]
            return result
        else:
            return None

    @Sessioner.dbconnect
    def update_post(self, new_post: UpdatePostRequest, session) -> None:
        if new_post.user_id == session.query(Posts)\
                                      .filter(Posts.PostID==new_post.post_id)\
                                      .first()\
                                      .CreatorPostID\
        :
            session.query(Posts)\
                   .filter(Posts.PostID==new_post.post_id)\
                   .update({Posts.text: new_post.new_text})

    @Sessioner.dbconnect
    def delete_post(self, post_id: int, user_id: int, session) -> None:
        query = session.query(Posts)\
                       .filter(Posts.PostID == post_id)\
                       .first()
        if user_id == query.CreatorPostID:
            session.delete(query)