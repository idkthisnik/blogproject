import React, { useState } from 'react';
import SettingsModal from '../../modal/settingsModal';
import axios from 'axios';

const Settings: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [axiosResponseStatus, setAxiosResponseStatus] = useState(true)
  const [errorMessage, setErrorMesage] = useState('')

  const handleOpenModal = (option: string) => {
    setSelectedOption(option);
    setErrorMesage('')
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setErrorMesage('')
    setSelectedOption('');
  };

  const UpdateLogin = async (data: any) => {
    try {
        const response = await axios.put(`${process.env.REACT_APP_FASTAPI_DOMAIN}/my_profile/settings/change_login`, {
                login: data.login,
                password: data.password,
                new_login: data.newLogin
            });
        if (response.data === true) {
            setAxiosResponseStatus(true)
            return true
        } else {
            return false
        }

    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
            setErrorMesage(error.response.data.detail)
            setAxiosResponseStatus(false)
            return false
        } else {
            console.error('Error updating login:', error);
            setAxiosResponseStatus(false)
            return false
        }
    }
};

const UpdatePassword = async (data: any) => {
    try {
        const response = await axios.put(`${process.env.REACT_APP_FASTAPI_DOMAIN}/my_profile/settings/change_password`, {
                login: data.login,
                password: data.password,
                new_password: data.newPassword
            });
        if (response.data === true) {
            setAxiosResponseStatus(true)
            return true
        } else {
            return false
        }

    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
            setErrorMesage(error.response.data.detail)
            setAxiosResponseStatus(false)
            return false
        } else {
            console.error('Error updating password:', error);
            setAxiosResponseStatus(false)
            return false
        }
    }
};


const UpdateEmail = async (data: any) => {
    try {
        const response = await axios.put(`${process.env.REACT_APP_FASTAPI_DOMAIN}/my_profile/settings/change_email`, {
                login: data.login,
                password: data.password,
                new_email: data.newEmail
            });
        if (response.data === true) {
            setAxiosResponseStatus(true)
            return true
        } else {
            return false
        }

    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
            setErrorMesage(error.response.data.detail)
            setAxiosResponseStatus(false)
            return false
        } else {
            console.error('Error updating email:', error);
            setAxiosResponseStatus(false)
            return false
        }
    }
};

const DeleteAccount = async (data: any) => {
    try {
        const response = await axios.delete(`${process.env.REACT_APP_FASTAPI_DOMAIN}/my_profile/settings/delete_account`, {
            data: {
                login: data.login,
                password: data.password
            }
            });
        if (response.data === true) {
            setAxiosResponseStatus(true)
            return true
        } else {
            return false
        }

    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
            setErrorMesage(error.response.data.detail)
            setAxiosResponseStatus(false)
            return false
        } else {
            console.error('Error deleting account:', error);
            setAxiosResponseStatus(false)
            return false
        }
    }
};

  const handleModalSubmit = (data: any) => {
    if (data.newLogin) { 
        return UpdateLogin(data)
    } else if (data.newPassword) {
        return UpdatePassword(data)
    } else if (data.newEmail) {
        return UpdateEmail(data)
    } else {
        return DeleteAccount(data)
    }
  };

  return (
    <div className="flex p-8">
      <div className="flex flex-col justify-center items-center h-screen w-full">
        <div className="flex flex-col items-center space-y-5">
            <button className="flex items-center justify-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-indigo-500 p-2 bg-indigo-500 text-white w-48" onClick={() => handleOpenModal('change login')}>Change Login</button>
            <button className="flex items-center justify-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-indigo-500 p-2 bg-indigo-500 text-white w-48" onClick={() => handleOpenModal('change password')}>Change Password</button>
            <button className="flex items-center justify-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-indigo-500 p-2 bg-indigo-500 text-white w-48" onClick={() => handleOpenModal('change email')}>Change Email</button>
            <button className="flex items-center justify-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-indigo-500 p-2 bg-indigo-500 text-white w-48" onClick={() => handleOpenModal('delete account')}>Delete Account</button>
            <a className="flex items-center justify-center space-x-1 hover:border-black hover:border-1 focus:outline-none border rounded-full border-deep-purple p-2 bg-deep-purple text-white w-48" href="/my-profile/">Back</a>
        </div>
    </div>
      <SettingsModal isOpen={isModalOpen} onClose={handleCloseModal} onSubmit={handleModalSubmit} option={selectedOption} errorMessage={errorMessage} setErrorMessage={setErrorMesage} />
    </div>
  );
};

export default Settings;