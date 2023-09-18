import { useState, useEffect } from "react";
import axios from "axios";
import Tick from "../../images/tick-svgrepo-com.svg"
import Cross from "../../images/cross-svgrepo-com.svg"

import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom'

import { useDispatch } from 'react-redux'
import { setCredentials } from '../../features/auth/authSlice'
import { useRegistrationMutation } from "../../features/auth/authRegistrationSlice";


const USER_REGEX = /^[a-zA-Z_][a-zA-Z0-9_-]{3,15}$/;
const PWD_REGEX = /^[a-zA-Z][a-zA-Z0-9]{7,31}$/;
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;


const Register = () => {
    const [user, setUser] = useState('');
    const [validName, setValidName] = useState(false);

    const [pwd, setPwd] = useState('');
    const [validPwd, setValidPwd] = useState(false);

    const [matchPwd, setMatchPwd] = useState('');
    const [validMatch, setValidMatch] = useState(false);

    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);

    const [errMsg, setErrMsg] = useState('');
    const [success, setSuccess] = useState(false);

    const navigate = useNavigate()
    const [registration, { isLoading }] = useRegistrationMutation()
    const dispatch = useDispatch()


    useEffect(() => {
        setValidName(USER_REGEX.test(user));
    }, [user])

    useEffect(() => {
        setValidPwd(PWD_REGEX.test(pwd));
        setValidMatch(pwd === matchPwd);
    }, [pwd, matchPwd])

    useEffect(() => {
        setValidEmail(EMAIL_REGEX.test(email));
    }, [email])

    useEffect(() => {
        setErrMsg('');
    }, [user, pwd, matchPwd])

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const v1 = USER_REGEX.test(user);
        const v2 = PWD_REGEX.test(pwd);
        if (!v1 || !v2) {
            setErrMsg("Invalid Entry");
            return;
        }
        try {
            const userData = await registration({ username: user, entered_password: pwd, email: email}).unwrap()

            if (userData.access_token) {
                setUser('');
                setPwd('');
                setMatchPwd('');
                setEmail('');
                setSuccess(true);

                setTimeout(() => {
                    Cookies.set('token', userData.access_token);
                    Cookies.set('refresh_token', userData.refresh_token);
                    dispatch(setCredentials({ userId: userData.userId, accessToken: userData.access_token }))
                    navigate('/homepage')  
                  }, 3000);
            }
        } catch (e: any) {
            if (!e?.data) {
              setErrMsg('No Server Response');
            } else if (e.status === 403) {
              setErrMsg(e.data.detail);
            } else if (e.status === 422) {
              setErrMsg('Oops! Not correct format!')  
            } else {
              setErrMsg('Registration Failed');
            }
        }
    }

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white shadow-lg p-8 rounded-lg w-full sm:w-96">
                {success ? (
                    <section>
                        <h1 className="text-2xl font-bold mb-4">Success! Redirecting...</h1>
                    </section>
                ) : (
                    <div>
                        <p  className={`text-red-500 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                        <h1 className="text-2xl font-bold mb-4 text-center">Sign Up</h1>
                        <form onSubmit={handleSubmit}>
                            <div>
                                <div className="flex items-center mb-1">
                                    Username:
                                    <img id="some-id" src={Tick} alt="tick" className={validName ? "visible w-5 h-5" : "hidden"} />
                                    <img id="some-id" src={Cross} alt="cross"className={validName || !user ? "hidden" : "visible w-5 h-5"} />
                                </div>
                                <input
                                    className="w-full border border-black p-1 rounded-lg mb-2"
                                    type="text"
                                    id="username"
                                    autoComplete="off"
                                    onChange={(e) => setUser(e.target.value)}
                                    value={user}
                                    required
                                    aria-invalid={validName ? "false" : "true"}
                                    aria-describedby="uidnote"
                                />
                                <p id="uidnote" className={user && !validName ? "visible bg-indigo-500 text-white rounded-lg p-1 mt-2" : "hidden"}>
                                    4 to 16 characters.<br />
                                    Must begin with a letter or '_'.<br />
                                    Letters, numbers, underscores, hyphens allowed.
                                </p>
                            </div>

                            <div>
                                <div className="flex items-center mb-1">
                                    Password:
                                    <img id="some-id" src={Tick} alt="tick" className={validPwd ? "visible w-5 h-5" : "hidden"} />
                                    <img id="some-id" src={Cross} alt="cross" className={validPwd || !pwd ? "hidden" : "visible w-5 h-5"} />
                                </div>
                                <input
                                    className="w-full border border-black p-1 rounded-lg mb-2"
                                    type="password"
                                    id="password"
                                    onChange={(e) => setPwd(e.target.value)}
                                    value={pwd}
                                    required
                                    aria-invalid={validPwd ? "false" : "true"}
                                    aria-describedby="pwdnote"
                                />
                                <p id="pwdnote" className={pwd && !validPwd ? "visible bg-indigo-500 text-white rounded-lg p-1 mt-2" : "hidden"}>
                                    8 to 32 characters.<br />
                                    Must include uppercase and lowercase letters, a number.<br />
                                </p>
                            </div>

                            <div>
                                <div className="flex items-center mb-1">
                                    Confirm Password:
                                    <img id="some-id" src={Tick} alt="tick" className={validMatch && matchPwd ? "visible w-5 h-5" : "hidden"} />
                                    <img id="some-id" src={Cross} alt="cross" className={validMatch || !matchPwd ? "hidden" : "visible w-5 h-5"} />
                                </div>
                                <input
                                    className="w-full border border-black p-1 rounded-lg mb-2"
                                    type="password"
                                    id="confirm_pwd"
                                    onChange={(e) => setMatchPwd(e.target.value)}
                                    value={matchPwd}
                                    required
                                    aria-invalid={validMatch ? "false" : "true"}
                                    aria-describedby="confirmnote"
                                />
                                <p id="confirmnote" className={matchPwd && !validMatch ? "visible bg-indigo-500 text-white rounded-lg p-1 mt-2" : "hidden"}>
                                    Must match the first password input field.
                                </p>
                            </div>

                            <div>
                                <div className="flex items-center mb-1">
                                    Email:
                                    <img id="some-id" src={Tick} alt="tick" className={validEmail ? "visible w-5 h-5" : "hidden"} />
                                    <img id="some-id" src={Cross} alt='cross' className={validEmail || !email ? "hidden" : "visible w-5 h-5"} />
                                </div>
                                <input
                                    className="w-full border border-black p-1 rounded-lg mb-2"
                                    type="email"
                                    id="email"
                                    onChange={(e) => setEmail(e.target.value)}
                                    value={email}
                                    required
                                    aria-invalid={validEmail ? "false" : "true"}
                                    aria-describedby="emailnote"
                                />
                                <p id="emailnote" className={email && !validEmail ? "visible bg-indigo-500 text-white rounded-lg p-1 mt-2" : "hidden"}>
                                    Your email has inccoret format! <br />
                                </p>
                            </div>
                            <div className="flex justify-between">
                                <button
                                    className={`bg-blue-500 text-white mt-4 py-2 px-4 rounded ${(!validName || !validPwd || !validMatch) && "opacity-50 cursor-not-allowed"}`}
                                    disabled={!validName || !validPwd || !validMatch}
                                >
                                    Sign Up
                                </button>
                                <p className="mt-4">
                                    Already registered?<br />
                                    <span className="line">
                                        <a href="/login" className="text-blue-500">Sign In</a>
                                    </span>
                                </p>
                            </div>
                        </form>
                    </div>
                )}
            </div>
       </div>
    )
}

export default Register

export {}