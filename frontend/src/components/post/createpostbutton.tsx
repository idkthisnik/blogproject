import React, { useState } from 'react';
import axios from 'axios';
import { Post } from './posts';

interface CreatePostProps {
    userId: number;
    changePostsError: () => void
    setPosts: React.Dispatch<React.SetStateAction<Post[]>>;
    setPostRatings: React.Dispatch<React.SetStateAction<{ postId: number; userId: number; like: boolean; dislike: boolean; }[]>>;
}

const CreatePost: React.FC<CreatePostProps> = ({ userId, changePostsError, setPosts, setPostRatings}) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [postText, setPostText] = useState('');
    const [errMsg, setErrMsg] = useState('');

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setErrMsg('')
        setPostText('');
    };

    const handleSubmit = async () => {
        try {
            const response = await axios.post(`${process.env.REACT_APP_FASTAPI_DOMAIN}/posts/create`, {
                user_id: userId,
                post_text: postText
            });

            const newPost = {
                ...response.data,
                comments_count: 0,
                post_rating: 0,
                following: false
            };

            const newPostRating = {
                postId: newPost.post_id,
                userId: userId,
                like: false,
                dislike: false
            };
    
            setPosts(posts => [newPost, ...posts]);
            setPostRatings(ratings => [newPostRating, ...ratings])
            changePostsError()
            
            closeModal();
        } catch (e: any) {
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
                Create Post
            </button>

            {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                    <div className="bg-white p-8 rounded-lg">
                        <p  className={`text-red-500 mb-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                        <textarea
                            className="w-full border p-2 mb-4"
                            placeholder="Enter your post text"
                            value={postText}
                            onChange={(e) => setPostText(e.target.value)}
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

export default CreatePost;