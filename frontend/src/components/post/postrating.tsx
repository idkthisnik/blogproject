import axios from 'axios';
import { Post } from './posts';

export const handleRating = (
  postId: number,
  userId: number,
  RatingReceiverID: number,
  posts: Post[],
  postRatings: { postId: number; userId: number; like: boolean; dislike: boolean }[],
  setPostRatings: React.Dispatch<React.SetStateAction<{ postId: number; userId: number; like: boolean; dislike: boolean }[]>>,
  setPosts: React.Dispatch<React.SetStateAction<Post[]>>,
  ratingValue: 'like' | 'dislike'
) => {
  const rateInfo = {
    user_id: userId,
    rating_receiver: RatingReceiverID,
    post_id: postId,
    rating_value: ratingValue
  };


  axios.post(`${process.env.REACT_APP_BACKEND_ADRESS}/posts/${postId}/rate`, rateInfo)
    .then(response => {
      const updatedPosts = posts.map(post => {
        if (post.post_id === postId) {
          let ratingChange: number = 0
          if (ratingValue === 'like') {
            if (postRatings.some(rating => rating.postId === postId && rating.like === true)) {
              ratingChange = -4;
            } else if (postRatings.some(rating => rating.postId === postId && rating.like === false  && rating.dislike === false)) {
              ratingChange = 4;
            } else if (postRatings.some(rating => rating.postId === postId && rating.like === false && rating.dislike === true)) {
              ratingChange = 6;
            }
          } else if (ratingValue === 'dislike'){
            if (postRatings.some(rating => rating.postId === postId && rating.dislike === true)) {
              ratingChange = 2;
            } else if (postRatings.some(rating => rating.postId === postId && rating.dislike === false && rating.like === false)) {
              ratingChange = -2;
            } else if (postRatings.some(rating => rating.postId === postId && rating.dislike === false && rating.like === true)) {
              ratingChange = -6;
            }
          }

          return {
            ...post,
            post_rating: post.post_rating + ratingChange
          };
        }
        return post;
      });
      setPosts(updatedPosts);


      if (ratingValue === 'like') {
        handleLike(postId, postRatings, setPostRatings);
      } else if (ratingValue === 'dislike') {
        handleDislike(postId, postRatings, setPostRatings);
      }
    })
    .catch(error => {
      console.error('Error rating post:', error);
    });
};



export const handleLike = (postId: number,
                           postRatings:{ postId: number; userId: number; like: boolean; dislike: boolean }[],
                           setPostRatings: React.Dispatch<React.SetStateAction<{ postId: number; userId: number; like: boolean; dislike: boolean }[]>>) => {
  const updatedRatings = postRatings.map(rating => {
    if (rating.postId === postId && rating.like === true) {
      return { ...rating, like: false, dislike: false };
    }
    else if (rating.postId === postId && rating.like === false) {
      return { ...rating, like: true, dislike: false };
    }
    return rating;
  });

  setPostRatings(updatedRatings);
};

export const handleDislike = (postId: number,
                              postRatings:{ postId: number; userId: number; like: boolean; dislike: boolean }[],
                              setPostRatings: React.Dispatch<React.SetStateAction<{ postId: number; userId: number; like: boolean; dislike: boolean }[]>>) => {
  const updatedRatings = postRatings.map(rating => {
    if (rating.postId === postId && rating.dislike === true) {
      return { ...rating, like: false, dislike: false };
    }
    else if (rating.postId === postId && rating.dislike === false) {
      return { ...rating, like: false, dislike: true };
    }
    return rating;
  });

  setPostRatings(updatedRatings);
};