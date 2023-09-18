import React from 'react';
import FunnyEmoji from "../../images/smile-1-svgrepo-com.svg"

const PostDeletedPage = () => {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <div className="text-center">
                <h1 className='text-2xl'>Post was succsessfully deleted!</h1>
                <p className="text-l">Now, we are redirecting you to homepage!</p>
                <div className="flex items-center justify-center mt-2">
                    <img id="some-id" src={FunnyEmoji} alt="Crying Emoji" className="w-10 h-10" />
                </div>
            </div>
        </div>

    );
};

export default PostDeletedPage;