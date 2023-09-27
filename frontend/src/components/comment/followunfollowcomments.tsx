import axios from 'axios';
import { Comment } from './comments';

export const isFollowed = async (userId: number, subscriberId: number, post_id: number, comment_id: number) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_FASTAPI_DOMAIN}/subscription/follow-unfollow/is-followed`, {
        user_id: userId,
        subscriber_id: subscriberId,
      });
      
      return response.data
    } catch (error) {
      console.error('Error following/unfollowing:', error);
      return false; 
    }
};


export const handleFollowUnfollow = async (creatorId: number, subscriberId: number, setComments: React.Dispatch<React.SetStateAction<Comment[]>>, post_id: number, comment_id: number) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_FASTAPI_DOMAIN}/subscription/follow-unfollow`, {
        user_id: creatorId, 
        subscriber_id: subscriberId,
      });
      setComments(prevComments => 
        prevComments.map(comment => 
          comment.creator_id === creatorId 
            ? { ...comment, following: !comment.following } 
            : comment
        )
      );
    } catch (error) {
      console.error('Error following:', error);
    }
  };