import React, { useState, useEffect, ReactNode } from 'react';
import { useDispatch } from 'react-redux';
import Cookies from 'js-cookie';
import jwt_decode from 'jwt-decode';
import { useRefreshMutation } from '../../features/auth/authRefreshSlice';
import { setCredentials } from '../../features/auth/authSlice';

interface DecodedToken {
  userId: number;
  expires: number;
}
interface PreloadDataProps {
  children: ReactNode;
}

const PreloadData: React.FC<PreloadDataProps> = ({ children }) => {
  const dispatch = useDispatch();
  const [refresh, { isLoading }] = useRefreshMutation();
  const [isDataLoaded, setDataLoaded] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const tokenFromCookie = Cookies.get('token');

      if (tokenFromCookie) {
        try {
          const decodedToken: DecodedToken = jwt_decode(tokenFromCookie);
          const currentTime = Math.floor(Date.now() / 1000);

          if (decodedToken.expires && decodedToken.expires < currentTime) {
            const user_id = decodedToken.userId;
            const userData = await refresh({ user_id, refresh_token: Cookies.get('refresh_token')}).unwrap();

            if (userData.access_token === null) {
              Cookies.remove('token');
              Cookies.remove('refresh_token');
              dispatch(setCredentials({ userId: null, accessToken: null }));

            } else {
              Cookies.set('token', userData.access_token);
              dispatch(setCredentials({ userId: decodedToken.userId, accessToken: tokenFromCookie }));
            }
          } else {
            dispatch(setCredentials({ userId: decodedToken.userId, accessToken: tokenFromCookie }));
          }

          setDataLoaded(true);  
        } catch (error) {
          console.error('Error decoding JWT token:', error);
        }
      }
      setDataLoaded(true); 
    };

    fetchData();
  }, [dispatch, refresh]);

  return isDataLoaded ? <>{children}</> : null;
};

export default PreloadData;