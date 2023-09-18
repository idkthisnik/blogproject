import React from 'react';
import CryingEmoji from "../images/crying-svgrepo-com.svg"
import Header from '../components/common/header';

const NotFoundPage = () => {
    return (
        <>
            <Header />
            <div className="flex flex-col items-center justify-center h-screen">
                <div className="text-center">
                    <h1 className='text-2xl'>Page Not Found</h1>
                    <p className="text-l">Sorry, the page you're looking for does not exist!</p>
                    <div className="flex items-center justify-center mt-2">
                        <img id="some-id" src={CryingEmoji} alt="Crying Emoji" className="w-10 h-10" />
                    </div>
                </div>
            </div>
        </>
    );
};

export default NotFoundPage;