import { useState } from "react";
import axios from "axios";
import { Post } from "../components/post/posts";

interface UpdatePostProps {
    userId: number;
    postId: number;
    setPosts: React.Dispatch<React.SetStateAction<Post[]>>;
}

const UpdatePost: React.FC<UpdatePostProps> = ({ userId, postId, setPosts}) => {
    const [updateModal, setUpdateModal] = useState(false)
    const [errMsg, setErrMsg] = useState('')
    const [postText, setPostText] = useState('');

    const openModal = () => {
        setUpdateModal(true)
      }
    
    const closeModal = () => {
        setUpdateModal(false)
      }

      const handleUpdatePost = async () => {
        try {
            const response = await axios.put(`${process.env.REACT_APP_FASTAPI_DOMAIN}/posts/${postId}/update`, {
                user_id: Number(userId), 
                post_id: Number(postId),
                new_text: postText 
            });
            setPosts((prevPosts) =>
                prevPosts.map((post) => {
                    if (post.post_id === postId) {
                        return { ...post, post_text: postText };
                    }
                    return post;
                })
            );
            closeModal()
    
        } catch (e: any) {
            setErrMsg(e);
            console.error('Error updating post:', e);
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
                        value={postText}
                        onChange={(e) => setPostText(e.target.value)}
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


export default UpdatePost;