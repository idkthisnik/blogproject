import axios from 'axios';
import { Post } from './posts';

export const isFollowed = async (userId: number, subscriberId: number) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_ADRESS}/subscription/follow-unfollow/is-followed`, {
        user_id: userId,
        subscriber_id: subscriberId,
      });
      
      return response.data
    } catch (error) {
      console.error('Error following/unfollowing:', error);
      return false; 
    }
};


export const handleFollowUnfollow = async (creatorId: number, subscriberId: number, setPosts: React.Dispatch<React.SetStateAction<Post[]>>) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_ADRESS}/subscription/follow-unfollow`, {
        user_id: creatorId, 
        subscriber_id: subscriberId,
      });
      setPosts(prevPosts => 
        prevPosts.map(post => 
          post.post_creator_id === creatorId 
            ? { ...post, following: !post.following } 
            : post
        )
      );
    } catch (error) {
      console.error('Error following:', error);
    }
  };