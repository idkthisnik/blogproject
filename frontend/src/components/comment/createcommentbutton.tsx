import React, { useState } from 'react';
import axios from 'axios';
import { Comment } from './comments';

interface CreateCommentProps {
    userId: number;
    postId: number;
    setComments: React.Dispatch<React.SetStateAction<Comment[]>>;
    setCommentRatings: React.Dispatch<React.SetStateAction<{ commentId: number; userId: number; like: boolean; dislike: boolean; }[]>>;
}

const CreateComment: React.FC<CreateCommentProps> = ({ userId, postId, setComments, setCommentRatings}) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [commentText, setCommentText] = useState('');
    const [errMsg, setErrMsg] = useState('');

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setCommentText('');
        setErrMsg('')
    };

    const handleSubmit = async () => {
        try {
            const response = await axios.post(`${process.env.REACT_APP_FASTAPI_DOMAIN}/posts/${postId}/create_comment`, {
                user_id: userId,
                post_id: postId,
                comment_text: commentText
            });

            const newComment = {
                ...response.data,
                comment_rating: 0,
                following: false
            };

            const newCommentRating = {
                commentId: newComment.comment_id,
                userId: userId,
                like: false,
                dislike: false
            };
    
            setComments(comments => [newComment, ...comments]);
            setCommentRatings(ratings => [newCommentRating, ...ratings])
    
            closeModal();

        } catch (e: any) {
            console.log(e)
            if (e.message === "Network Error") {
                setErrMsg('No Server Response');
              } else if (e.response.status === 422) {
                setErrMsg(e.response.data.detail);
              } 
        }
    };
    

    return (
        <div className='flex justify-center items-center'>
            <button onClick={openModal} className="border rounded-full px-2 border-indigo-500 p-2 bg-indigo-500 text-white mt-2 hover:border-black hover:border-1">
                Create Comment
            </button>

            {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                    <div className="bg-white p-8 rounded-lg">
                        <p  className={`text-red-500 mb-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                        <textarea
                            className="w-full border p-2 mb-4"
                            placeholder="Enter your comment text"
                            value={commentText}
                            onChange={(e) => setCommentText(e.target.value)}
                        />
                        <div className="flex justify-between">
                            <button onClick={handleSubmit} className="border rounded-full px-2 border-indigo-500 p-2 bg-indigo-500 text-white mt-2 hover:border-black hover:border-1">
                                Submit
                            </button>
                            <button onClick={closeModal} className="border rounded-full px-2 border-deep-purple p-2 bg-deep-purple text-white mt-2 hover:border-black hover:border-1">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CreateComment;