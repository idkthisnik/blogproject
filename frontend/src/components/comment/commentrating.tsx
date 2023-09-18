import { useState } from 'react';
import axios from 'axios';
import { Comment } from './comments';

export const handleRating = (
  commentId: number,
  postId: number,
  userId: number,
  receiver_id: number,
  comments: Comment[],
  commentRatings: { commentId: number; userId: number; like: boolean; dislike: boolean }[],
  setCommentRatings: React.Dispatch<React.SetStateAction<{ commentId: number; userId: number; like: boolean; dislike: boolean }[]>>,
  setComments: React.Dispatch<React.SetStateAction<Comment[]>>,
  ratingValue: 'like' | 'dislike'
) => {
  const rateInfo = {
    user_id: userId,
    rating_receiver: receiver_id, 
    comment_id: commentId,
    rating_value: ratingValue
  };

  axios.post(`${process.env.REACT_APP_BACKEND_ADRESS}/posts/${postId}/${commentId}`, rateInfo)
    .then(response => {
      const updatedComments = comments.map(comment => {
        if (comment.comment_id === commentId) {
          let ratingChange: number = 0
          if (ratingValue === 'like') {
            if (commentRatings.some(rating => rating.commentId === commentId && rating.like === true)) {
              ratingChange = -4;
            } else if (commentRatings.some(rating => rating.commentId === commentId && rating.like === false  && rating.dislike === false)) {
              ratingChange = 4;
            } else if (commentRatings.some(rating => rating.commentId === commentId && rating.like === false && rating.dislike === true)) {
              ratingChange = 6;
            }
          } else if (ratingValue === 'dislike'){
            if (commentRatings.some(rating => rating.commentId === commentId && rating.dislike === true)) {
              ratingChange = 2;
            } else if (commentRatings.some(rating => rating.commentId === commentId && rating.dislike === false && rating.like === false)) {
              ratingChange = -2;
            } else if (commentRatings.some(rating => rating.commentId === commentId && rating.dislike === false && rating.like === true)) {
              ratingChange = -6;
            }
          }

          return {
            ...comment,
            comment_rating: comment.comment_rating + ratingChange
          };
        }
        return comment;
      });
      setComments(updatedComments);


      if (ratingValue === 'like') {
        handleLike(commentId, commentRatings, setCommentRatings);
      } else if (ratingValue === 'dislike') {
        handleDislike(commentId, commentRatings, setCommentRatings);
      }
    })
    .catch(error => {
      console.error('Error rating post:', error);
    });
};



export const handleLike = (commentId: number,
                           commentRatings: { commentId: number; userId: number; like: boolean; dislike: boolean }[],
                           setCommentRatings: React.Dispatch<React.SetStateAction<{ commentId: number; userId: number; like: boolean; dislike: boolean }[]>>) => {

  const updatedRatings = commentRatings.map(rating => {
    if (rating.commentId === commentId && rating.like === true) {
      return { ...rating, like: false, dislike: false };
    }
    else if (rating.commentId === commentId && rating.like === false) {
      return { ...rating, like: true, dislike: false };
    }
    return rating;
  });

  setCommentRatings(updatedRatings);
};

export const handleDislike = (commentId: number,
                              commentRatings: { commentId: number; userId: number; like: boolean; dislike: boolean }[],
                              setCommentRatings: React.Dispatch<React.SetStateAction<{ commentId: number; userId: number; like: boolean; dislike: boolean }[]>>) => {

  const updatedRatings = commentRatings.map(rating => {
    if (rating.commentId === commentId && rating.dislike === true) {
      return { ...rating, like: false, dislike: false };
    }
    else if (rating.commentId === commentId && rating.dislike === false) {
      return { ...rating, like: false, dislike: true };
    }
    return rating;
  });

  setCommentRatings(updatedRatings);
};