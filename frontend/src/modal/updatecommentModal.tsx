import { useState } from "react";
import axios from "axios";
import { Comment } from "../components/comment/comments";

interface UpdatePostProps {
    postId: number,
    userId: number;
    commentId: number;
    setComments: React.Dispatch<React.SetStateAction<Comment[]>>;
}

const UpdateComment: React.FC<UpdatePostProps> = ({ postId, userId, commentId, setComments}) => {
    const [updateModal, setUpdateModal] = useState(false)
    const [errMsg, setErrMsg] = useState('')
    const [commentText, setCommentText] = useState('');

    const openModal = () => {
        setUpdateModal(true)
      }
    
    const closeModal = () => {
        setUpdateModal(false)
      }

      const handleUpdatePost = async () => {
        try {
            const response = await axios.put(`${process.env.REACT_APP_FASTAPI_DOMAIN}/posts/${postId}/${commentId}/update`, {
                user_id: userId, 
                comment_id: commentId,
                new_text: commentText
            });

            setComments((prevComments) =>
                prevComments.map((comment) => {
                    if (comment.comment_id === commentId) {
                        return { ...comment, comment_text: commentText };
                    }
                    return comment;
                })
            );
            closeModal()
    
        } catch (e: any) {
            setErrMsg(e);
            console.error('Error updating comment:', e);
        }
    };

    return (
        <div className='flex justify-center items-center'>
        <button onClick={openModal} className="border bg-indigo-500 text-white rounded-full px-2 p-2 hover:border-black hover:border-1">
            Update Post
        </button>

        {updateModal && (
            <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                <div className="bg-white p-8 rounded-lg">
                    <p  className={`text-red-500 mb-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                    <textarea
                        className="w-full border p-2 mb-4"
                        placeholder="Enter new post text"
                        value={commentText}
                        onChange={(e) => setCommentText(e.target.value)}
                    />
                    <div className="flex justify-between">
                        <button onClick={handleUpdatePost} className="border rounded-full px-2 border-indigo-500 p-2 bg-indigo-500 text-white mt-2 hover:border-black hover:border-1">
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
    )
  }


export default UpdateComment;