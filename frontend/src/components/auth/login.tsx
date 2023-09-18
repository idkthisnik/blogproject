import Cookies from 'js-cookie';

import { useState, useEffect } from 'react'

import { useDispatch } from 'react-redux'
import { setCredentials } from '../../features/auth/authSlice'
import { useLoginMutation } from '../../features/auth/authApiSlice'


const Login = () => {

    const [username, setUsername] = useState('')
    const [entered_password, setEntered_password] = useState('')
    const [errMsg, setErrMsg] = useState('')

    const [login, { isLoading }] = useLoginMutation()
    const dispatch = useDispatch()

    useEffect(() => {
        setErrMsg('')
    }, [username, entered_password])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        try {
            const userData = await login({ username, entered_password }).unwrap()

            if (userData.access_token) {
                Cookies.set('token', userData.access_token);
                Cookies.set('refresh_token', userData.refresh_token);

                dispatch(setCredentials({ userId: userData.userId, accessToken: userData.access_token }))

                setUsername('')
                setEntered_password('')
            } 
        
        } catch (e: any) {
            console.log(e)
            if (!e?.data) {
              setErrMsg('No Server Response');
            } else if (e.status === 401) {
              setErrMsg(e.data.detail);
            } else if (e.status === 422) {
              setErrMsg('Oops! Not correct format!')  
            } else {
              setErrMsg('Login Failed');
            }
        }
    }

    const handleUserInput = (e: React.FormEvent<HTMLInputElement>) => setUsername(e.currentTarget.value)

    const handlePwdInput = (e: React.FormEvent<HTMLInputElement>) => setEntered_password(e.currentTarget.value)

    const content = isLoading ? <h1>Loading...</h1> : (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white shadow-lg p-8 rounded-lg w-full sm:w-96">
                <section className="login">
                    <h1 className="text-2xl font-bold mb-4 text-center">Login</h1>

                    <form onSubmit={handleSubmit}>
                        <div className="flex items-center mb-1">
                            <label htmlFor="username">Username:</label>
                        </div>
                        <input
                            className="w-full border border-black p-1 rounded-lg mb-2"
                            type="text"
                            id="username"
                            value={username}
                            onChange={handleUserInput}
                            autoComplete="off"
                            required
                        />

                        <div className="flex items-center mb-1">
                            <label htmlFor="password">Password:</label>
                        </div>

                        <input
                            className="w-full border border-black p-1 rounded-lg mb-2"
                            type="password"
                            id="password"
                            onChange={handlePwdInput}
                            value={entered_password}
                            required
                        />
                        <div className='flex justify-between'>
                            <button
                            className={`bg-blue-500 text-white mt-4 py-2 px-4 rounded border border-transparent hover:border-black`}
                            >
                                Sign In
                            </button>
                            <p  className={`text-red-500 mt-4 py-2 px-4 ${errMsg ? "" : "hidden"}`} aria-live="assertive">{errMsg}</p>
                        </div>
                    </form>
                </section>
            </div>
        </div>
    )

    return content
}
export default Login