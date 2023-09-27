import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import SearchModal from '../../modal/searchModal';

export interface User {
  user_id: number;
  login: string;
}

const SearchBar = () => {
  const [value, setValue] = useState('')
  const [users, setUsers] = useState<User[]>([]);
  const [searchModal, setSearchModal] = useState(false)
  

  const getUsers = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.get(`${process.env.REACT_APP_FASTAPI_DOMAIN}/users`);
      setUsers(response.data);
    } catch (error) {
      console.error("Ошибка при запросе пользователей:", error);
    }
  };


    const filteredUsers = users.filter(user => {
      const username = user.login.toLowerCase();
      const search = value.toLowerCase();
      return username.includes(search);
    });

  const handleSearchSubmit = (event: React.FormEvent) => {
    if (value.length !== 0) {
      event.preventDefault();
      getUsers(event)
      setSearchModal(true)
     } else {
      event.preventDefault();
     }
    }
  
  return (
    <div className="flex items-center">
    <form onSubmit={handleSearchSubmit} className="flex  space-x-1">
      <input
        type="text"
        placeholder="Search user..."
        className="block w-full px-4 py-2 text-purple-700 bg-white border rounded-full focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
        onChange={(e) => setValue(e.target.value)}
      />
      <button type="submit" className="px-4 text-white bg-purple-600 rounded-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-7 h-7"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
        </svg>
      </button>
    </form>
    {searchModal && (
      <SearchModal filteredUsers={filteredUsers} setSearchModal={setSearchModal}/>
      )}
    </div>
  );
 };

export default SearchBar;