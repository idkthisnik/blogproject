import { useState, useEffect } from 'react'
import axios from 'axios'
import { handleRating } from './commentrating'
import { isFollowed, handleFollowUnfollow} from './followunfollowcomments'
import CreateComment from './createcommentbutton'
import CryingEmoji from "../../images/crying-svgrepo-com.svg"
import UpdateComment from '../../modal/updatecommentModal'


export interface Comment {
    comment_id: number
    creator_id: number
    comment_text: string
    comment_time: string 
    comment_creator: string 
    comment_rating: number
    following: boolean 
}

interface CommentProps {
    user_id: number
    post_id: number
}

const CommentsList: React.FC<CommentProps> = ({user_id, post_id}) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentRatings, setCommentRatings] = useState<{ commentId: number; userId: number; like: boolean; dislike: boolean }[]>([]);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1)
  const size = 4


  const handleNextPage = () => {
    if (page + 1 <= pages) {
      fetchComments(page + 1); 
      setPage(page + 1);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      fetchComments(page - 1);
      setPage(page - 1);
    }
  };

  useEffect(() => {
    fetchComments(page);
  }, []);

  const fetchComments = async (current_page: number) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_ADRESS}/posts/${post_id}/comments?page=${current_page}&size=${size}`);
      const userId = user_id;

      setPages(response.data.pages);

      const updatedComments = await Promise.all(
        response.data.items.map(async (comment: Comment) => {
          const rated = await commentRatedByUser(comment, userId);
          const following = await isFollowed(comment.creator_id, userId, post_id, comment.comment_id);
          
          return { ...comment, rated, following };
        })
      );
      
      setComments(updatedComments);

    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const handleRemoveComment = async (userId: number, commentId: number) => {
    try {
      const response = await axios.delete(`${process.env.REACT_APP_BACKEND_ADRESS}/posts/${post_id}/${commentId}`, {
        data: {
          user_id: Number(userId), 
          comment_id: Number(commentId),
        }  
      });
      setComments(prevComments => prevComments.filter(comment => comment.comment_id !== commentId));


    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };

  const commentRatedByUser = async (comment: Comment, userId: number) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_ADRESS}/posts/${post_id}/commentRatedByUser?comment_id=${comment.comment_id}&user_id=${userId}`)
      
      setCommentRatings(prevCommentRatings => [
        ...prevCommentRatings,
        {
          commentId: comment.comment_id,
          userId: userId,
          like: response.data.rating_value === 4,
          dislike: response.data.rating_value === -2,
        },
      ]);
  
      return response.data.rating_existence;
    } catch (error) {
      console.error('Ошибка при проверке наличия рейтинга:', error);
      return false;
    }
  };

  if (comments.length === 0) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-1 xl:grid-cols-1 gap-4 mt-4">
            <div className="mx-auto w-full flex justify-between sm:w-1/2 md:w-1/3 lg:w-1/3 xl:w-1/3">
                <p className="text-2xl font-semibold">Comments:</p>
                <CreateComment userId={user_id} postId={Number(post_id)} setComments={setComments} setCommentRatings={setCommentRatings}/>
            </div>
            <div className="flex flex-col items-center justify-center my-10">
                <div className="text-center">
                    <h1 className='text-2xl'>Comments Not Found</h1>
                    <p className="text-l">There no comments to this post. Be fisrt!</p>
                    <div className="flex items-center justify-center mt-2">
                        <img id="some-id" src={CryingEmoji} alt="Crying Emoji" className="w-10 h-10" />
                    </div>
                </div>
            </div>
        </div>
    )
  }

  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-1 xl:grid-cols-1 gap-4 mt-4">
        <div className="mx-auto w-full flex justify-between sm:w-1/2 md:w-1/3 lg:w-1/3 xl:w-1/3">
            <p className="text-2xl font-semibold">Comments:</p>
            <CreateComment userId={user_id} postId={Number(post_id)} setComments={setComments} setCommentRatings={setCommentRatings}/>
        </div>
      {comments.map(comment => (
        <div key={comment.comment_id} 
          className="mx-auto w-full sm:w-1/2 md:w-1/3 lg:w-1/3 xl:w-1/3 border p-5 rounded shadow-md"
        >
            <div className="flex justify-between">
              <div>
                <a href={`${process.env.REACT_APP_ADRESS}/users/${comment.creator_id}`} className="font-bold hover:underline">
                    {comment.comment_creator}
                </a>
              </div>
              <div>
                {user_id !== comment.creator_id && (    
                  <button
                    onClick={() => handleFollowUnfollow(comment.creator_id, user_id, setComments, post_id, comment.comment_id)}
                    className={`border rounded-full px-2 border-indigo-500 p-2 hover:border-black hover:border-1 ${comment.following ? 'bg-white text-black' : 'bg-indigo-500 text-white'}`}
                  >
                    {comment.following ? 'Followed!' : 'Follow'}
                  </button>
                )}
                {user_id !== null && user_id === comment.creator_id && (
                <div className="flex justify-center mt-2 mb-4 items-center space-x-4 w-full">
                  <UpdateComment postId={post_id} userId={user_id} commentId={comment.comment_id} setComments={setComments}/>
                  <button
                    onClick={() => handleRemoveComment(comment.creator_id, comment.comment_id)}
                    className={`border bg-red-500 text-white rounded-full px-2 p-2 hover:border-black hover:border-1`}
                  >
                    Delete
                  </button>
                </div>
                )}
                </div>
            </div>
            <div className="flex justify-between mt-2">  
              <p className="mt-2">{comment.comment_text}</p>
              <p className="text-gray-500" title={comment.comment_time}>{comment.comment_time.split(' ')[0]}</p>
            </div>  
              <div className="flex justify-between mt-4">
                <div className="flex items-center space-x-4">
                    <button 
                    onClick={() => handleRating(comment.comment_id, post_id, user_id, comment.creator_id, comments, commentRatings, setCommentRatings, setComments, 'like')}
                    className={`flex items-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-indigo-500 p-2 bg-indigo-500 ${commentRatings.find(rating => rating.commentId === comment.comment_id && rating.like) ? 'text-red-500' : 'text-white'}`}
                    >
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" className="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16"> 
                        <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/> 
                    </svg>
                    </button>
                    
                    <button 
                    onClick={() => handleRating(comment.comment_id, post_id, user_id, comment.creator_id, comments, commentRatings, setCommentRatings, setComments, 'dislike')}
                    className={`flex items-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-deep-purple p-2 bg-deep-purple ${commentRatings.find(rating => rating.commentId === comment.comment_id && rating.dislike) ? 'text-black-500' : 'text-white'}`}
                    >
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" className="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16"> 
                        <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.378 1.378 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51.136.02.285.037.443.051.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.896 1.896 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2.094 2.094 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.162 3.162 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.823 4.823 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591z"/>
                    </svg>
                    </button>
                </div>
                <p className="text-sm text-gray-500 text-center mt-2">{`Rating: ${comment.comment_rating}`}</p>
        </div>
        </div>
      ))}
      <div className="flex justify-center mt-2 mb-4 items-center space-x-4 w-full">
          <button
            onClick={() => handlePrevPage()}
            className={`flex items-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-deep-purple p-2 bg-indigo-500 text-white`}
          >Previous Page
          </button>
          <p className="mt-2 text-xl text-decoration-line: underline">{page}</p>
          <button
            onClick={() => handleNextPage()}
            className={`flex items-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-deep-purple p-2 bg-indigo-500 text-white`}
          >Next Page

          </button>
      </div>
    </div>
  );
};

  
export default CommentsList;