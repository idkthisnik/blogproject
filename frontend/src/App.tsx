import React from 'react';
import Layout from './components/common/layout';
import HomePage from './pages/HomePage';
import {Route, Routes} from 'react-router-dom'
import MyProfilePage from './pages/MyProfilePage';
import ProfilePage from './pages/UserProfilePage';
import NotFoundPage from './pages/NonePage';
import SettingsPage from './pages/SettingsPage';
import PostPage from './pages/PostPage';
import RegistrationPage from './pages/RegistrationPage';
import LoginPage from './pages/LoginPage';
import RequireAuth from './features/auth/RequireAuth';
import RequireNotAuth from './features/auth/RequireNotAuth';



function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* public */}
        <Route element={<RequireNotAuth />}>
          <Route path='/registration' element={<RegistrationPage />} />
          <Route path='/login' element={<LoginPage />} />
        </Route>  
        
        <Route path="/" element={<HomePage />} />
        <Route path="/homepage" element={<HomePage />} />
        <Route path="*" element={<NotFoundPage />} />

        {/* private */}
        <Route element={<RequireAuth />}>
          <Route path="/my-profile" element={<MyProfilePage />} />
          <Route path="/users/:user_id" element={<ProfilePage />} />
          <Route path="/my-profile/settings" element={<SettingsPage />} />
          <Route path="/posts/:post_id" element={<PostPage />} />
        </Route>
      </Route>
    </Routes>
  )
}

export default App;
