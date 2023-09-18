import { User } from "../components/search/searchBar";
import Cross from "../images/cross-svgrepo-com.svg"

interface SearchModalProps {
    filteredUsers: User[] | [];
    setSearchModal: React.Dispatch<React.SetStateAction<boolean>>;
    }

const SearchModal: React.FC<SearchModalProps> = ({ filteredUsers, setSearchModal}) => {
    const closeModal = () => {
        setSearchModal(false)
    }

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
          <div className="bg-white p-8 rounded-lg border border-gray-300 w-96 relative">
            <button
              onClick={closeModal}
              className="absolute top-2 right-2 border rounded-full px-2 border-indigo-500 p-2 bg-white text-white hover:border-black hover:border-1"
            >
              <img src={Cross} alt="Cross" className="object-contain h-5 w-5" />
            </button>
            <div className="flex justify-center">
              <ul className="grid grid-cols-1 gap-2 mt-4 flex">
                {filteredUsers.length === 0 && (
                  <p
                    className={`text-red-500 mb-4 ${
                      'Users with your query does not found :(' ? "" : "hidden"
                    }`}
                    aria-live="assertive"
                  >
                    {'Users with your query does not found :('}
                  </p>
                )}
                {filteredUsers.map((user) => (
                  <a
                    key={user.user_id}
                    href={`${process.env.REACT_APP_ADRESS}/users/${user.user_id}`}
                    className="font-bold hover:underline text-black"
                  >
                    {user.login}
                  </a>
                ))}
              </ul>
            </div>
          </div>
        </div>
      );
  }


export default SearchModal;