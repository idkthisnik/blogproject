
import axios from "axios";
import { useState, useEffect } from "react";
import CryingEmoji from "../../images/crying-svgrepo-com.svg"
import { useSelector } from "react-redux";
import { selectCurrentUser } from "../../features/auth/authSlice";
import { isFollowed, handleFollowUnfollow } from "./handlesubscribe";

export interface ProfileInfoInterface {
    login: string
    rating: number
    subscriptions: number
    subscribers: number
    following: boolean | null
}



interface ProfileInfoProps {
    userId: number;
    onError: () => void;
}

const ProfileInfo: React.FC<ProfileInfoProps> = ({ userId, onError }) => {
    const [profileinfo, setProfileinfo] = useState<ProfileInfoInterface | null>(null);
    const [isError, setIsError] = useState(false);
    const current_userId = useSelector(selectCurrentUser)

    const [isSubscriptionsModalOpen, setIsSubscriptionsModalOpen] = useState(false);
    const [isSubscribersModalOpen, setIsSubscribersModalOpen] = useState(false);

    const [subscribersList, setSubscribersList] = useState<[]>([])
    const [subscriptionsList, setSubscriptionsList] = useState<[]>([])

    const [errMsg, setErrMsg] = useState('');

    const opencloseSubscriptionsModal = async () => {
        await SubscriptionsList();
        setIsSubscriptionsModalOpen(prev => !prev);
        setErrMsg('')
    };

    const opencloseSubscribersModal = async () => {
        await SubscribersList();
        setIsSubscribersModalOpen(prev => !prev);
        setErrMsg('')
    };

    const SubscribersList = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_ADRESS}/subscription/subscribers`, {
                params: {
                    user_id: userId
                }
            });

            await setSubscribersList(response.data);
        } catch (e: any) {
            console.log(e)
            if (e.message === "Network Error") {
                setErrMsg('No Server Response');
              } else if (e.response.status === 404) {
                setErrMsg(e.response.data.detail);
              } 
        }
    };

    const SubscriptionsList = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_ADRESS}/subscription/subscriptions`, {
                params: {
                    user_id: userId
                }
            });
            setSubscriptionsList(response.data);
        } catch (e: any) {
            console.log(e)
            if (e.message === "Network Error") {
                setErrMsg('No Server Response');
              } else if (e.response.status === 404) {
                setErrMsg(e.response.data.detail);
              } 
        }
    };



    const fetchProfileInfo = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_ADRESS}/${userId}/data`, {
                params: {
                    user_id: userId
                }
            });
            if (current_userId !== null) {
                const updatedProfile = { ...response.data, following: await isFollowed(userId, current_userId) };
                setProfileinfo(updatedProfile);
            }

        } catch (error) {
            if (axios.isAxiosError(error) && error.response?.status === 404) {
                onError()
                setIsError(true)
            } else {
                console.error('Error fetching profile info:', error);
            }
        }
    };

    useEffect(() => {
        fetchProfileInfo();
    }, []);


    if (isError && profileinfo === null) {
        return (
            <div className="flex flex-col items-center justify-center h-screen">
                <div className="text-center">
                    <p className="text-xl">Oops! User not found!</p>
                    <div className="flex items-center justify-center mt-2">
                        <img id="some-id" src={CryingEmoji} alt="Crying Emoji" className="w-10 h-10" />
                    </div>
                </div>
            </div>
        )
    }
    if (profileinfo !== null)  {

        return (
            <div className="flex justify-center items-center">
                <div className="w-3/5 mt-8 mb-4">
                    <div className="bg-gray-100 p-10 rounded-lg shadow-md flex justify-between">
                        <div className="ml-10">
                            <p className="text-2xl font-bold">{profileinfo.login}</p>
                            {current_userId && (
                                <button
                                onClick={() => handleFollowUnfollow(userId, current_userId, setProfileinfo)}
                                className={`border rounded-full px-2 border-indigo-500 p-2 hover:border-black hover:border-1 ${profileinfo.following ? 'bg-white text-black' : 'bg-indigo-500 text-white'}`}
                                >
                                {profileinfo.following ? 'Followed!' : 'Follow'}

                                </button>
                            )}
                        </div>
                        <div className="ml-10">
                            <p className="text-gray-800 mt-2">Rating: {profileinfo.rating}</p>
                            <div>
                                <p className="text-gray-800">Subscriptions: 
                                    <button onClick={opencloseSubscriptionsModal} className="text-blue-500 underline ml-1">
                                        {profileinfo.subscriptions}
                                    </button>
                                </p>
                                <p className="text-gray-800">Subscribers: 
                                    <button onClick={opencloseSubscribersModal} className="text-blue-500 underline ml-1">
                                        {profileinfo.subscribers}
                                    </button>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                {isSubscriptionsModalOpen && (
                    <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                        <div className="bg-white p-8 rounded-lg border border-gray-300">
                            <h2 className="text-xl font-semibold mb-4">Subscriptions</h2>
                            <p  className={`text-red-500 mb-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                            <ul className="grid grid-cols-1 gap-2 mt-4">
                            {Object.entries(subscriptionsList).map(([id, nickname]) => (
                                <a key={id} href={`${process.env.REACT_APP_ADRESS}/users/${id}`} className="font-bold hover:underline">
                                    {nickname}
                                </a>
                            ))}
                            </ul>
                            <button onClick={opencloseSubscriptionsModal} className="border rounded-full px-2 border-deep-purple p-2 bg-deep-purple text-white mt-2 hover:border-black hover:border-1">
                                Close
                            </button>
                        </div>
                    </div>
                )}

                {isSubscribersModalOpen && (
                    <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
                        <div className="bg-white p-8 rounded-lg border border-gray-300">
                            <h2 className="text-xl font-semibold mb-4">Subscribers</h2>
                            <p  className={`text-red-500 mb-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                            <ul className="grid grid-cols-1 gap-2 mt-4">
                            {Object.entries(subscribersList).map(([id, nickname]) => (
                                <a key={id} href={`${process.env.REACT_APP_ADRESS}/users/${id}`} className="font-bold hover:underline">
                                    {nickname}
                                </a>
                            ))}
                            </ul>
                            <button onClick={opencloseSubscribersModal} className="border rounded-full px-2 border-deep-purple p-2 bg-deep-purple text-white mt-2 hover:border-black hover:border-1">
                                Close
                            </button>
                        </div>
                    </div>
                )}

            </div>
        )
    }
    return null;
}

export default ProfileInfo