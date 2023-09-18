import { ProfileInfoInterface } from "./profileinfo";
import axios from "axios";


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

export const handleFollowUnfollow = async (
    userId: number,
    subscriberId: number,
    setProfileinfo: React.Dispatch<React.SetStateAction<ProfileInfoInterface | null>>
  ) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_ADRESS}/subscription/follow-unfollow`, {
        user_id: userId, 
        subscriber_id: subscriberId,
      });
      setProfileinfo(profile =>
            profile !== null && userId !== subscriberId
             ? { ...profile, following: !profile.following }
            : profile
        )
    } catch (error) {
      console.error('Error following:', error);
    }
  };