import axios from "axios";
import { useState, useEffect } from "react";

export interface MyProfileInfo {
    login: string;
    email: string;
    rating: number;
    subscriptions: number;
    subscribers: number;
}

interface MyProfileInfoProps {
    userId: number;
}


const MyProfileInfo: React.FC<MyProfileInfoProps> = ({userId}) => {
    const [myprofileinfo, setMyprofileinfo] = useState<MyProfileInfo>();

    const [isSubscriptionsModalOpen, setIsSubscriptionsModalOpen] = useState(false);
    const [isSubscribersModalOpen, setIsSubscribersModalOpen] = useState(false);

    const [subscribersList, setSubscribersList] = useState<[]>([])
    const [subscriptionsList, setSubscriptionsList] = useState<[]>([])

    const [errMsg, setErrMsg] = useState('');

    const opencloseSubscriptionsModal = () => {
        setIsSubscriptionsModalOpen(prev => !prev);
        setErrMsg('')
    };

    const opencloseSubscribersModal = () => {
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

            setSubscribersList(response.data);
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

            setMyprofileinfo(response.data);
        } catch (error) {
            console.error('Error fetching profile info:', error);
        }
    };

    useEffect(() => {
        fetchProfileInfo();
    }, []);


    useEffect(() => {
        if (isSubscriptionsModalOpen) {
            SubscriptionsList();
        }
    }, [isSubscriptionsModalOpen]);

    
    useEffect(() => {
        if (isSubscribersModalOpen) {
            SubscribersList();
        }
    }, [isSubscribersModalOpen]);

    if (!myprofileinfo) {
        return <div>Loading...</div>;
    }

    return (
        <div className="flex justify-center items-center">
            <div className="w-3/5 mt-8 mb-4">
                <div className="bg-gray-100 p-10 rounded-lg shadow-md flex justify-between">
                    <div className="ml-10">
                        <p className="text-2xl font-bold">{myprofileinfo.login}</p>
                        <p className="text-gray-600 mb-4">{myprofileinfo.email}</p>
                        <a
                            href="/my-profile/settings/"
                            className={`border rounded-full px-2 border-indigo-500 p-2 bg-indigo-500 text-white mt-2 hover:border-black hover:border-1`}
                        >
                            Settings
                        </a>
                    </div>
                    <div className="ml-10">
                        <p className="text-gray-800 mt-2">Rating: {myprofileinfo.rating}</p>
                        <div>
                            <p className="text-gray-800">Subscriptions: 
                                <button onClick={opencloseSubscriptionsModal} className="text-blue-500 underline ml-1">
                                    {myprofileinfo.subscriptions}
                                </button>
                            </p>
                            <p className="text-gray-800">Subscribers: 
                                <button onClick={opencloseSubscribersModal} className="text-blue-500 underline ml-1">
                                    {myprofileinfo.subscribers}
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


export default MyProfileInfo