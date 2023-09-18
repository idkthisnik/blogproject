import React from 'react'
import { Link } from 'react-router-dom'
import { selectTokenExists } from '../../features/auth/authSlice';
import Cookies from "js-cookie";
import { logOut } from '../../features/auth/authSlice';
import { useDispatch } from 'react-redux';
import { useState } from 'react';
import LogoutModal from '../../modal/logoutModal';
import { useSelector } from 'react-redux';
import { selectCurrentUser } from '../../features/auth/authSlice';
import { useLogoutMutation } from '../../features/auth/authLogoutSlice';
import SearchBar from '../search/searchBar';



const Header: React.FC = () => {
  const dispatch = useDispatch()
  const tokenExists = useSelector(selectTokenExists);
  const user_id = useSelector(selectCurrentUser)
  const [logout, { isLoading }] = useLogoutMutation()

  const [isOpen, setIsOpen] = useState(false)


  const handleOpenClose = () => {
    setIsOpen(prev => !prev)
  };

  const handleLogout = async () => {
    const logoutQuery = await logout({ user_id });
    Cookies.remove('token');
    Cookies.remove('refresh_token');
    await dispatch(logOut({}));
    setIsOpen(false);
  };

  return (
    <div className="bg-indigo-500 text-indigo-50">
      <header>
        <div className="flex justify-between items-center px-8 py-4">
          <Link to="/homepage">Homepage</Link>
          <SearchBar />
          {tokenExists ? (
            <div className='flex justify-between'>
              <Link to="/my-profile" className='mr-5'>My Profile</Link>
              <button onClick={handleOpenClose}>LogOut</button>
            </div>
          ) : (
            <div className='flex justify-between'>
              <Link to="/login" className='mr-5'>Sign In</Link>
              <Link to="/registration">Sign Up</Link>
            </div>
          )}
        </div>
        <LogoutModal isOpen={isOpen} onOpenClose={handleOpenClose} onLogout={handleLogout}/>
      </header>
    </div>
  );
}

export default Header