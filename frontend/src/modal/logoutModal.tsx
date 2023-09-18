import React from 'react';

interface LogoutModalProps {
  isOpen: boolean;
  onOpenClose: () => void;
  onLogout: () => void;
}

const LogoutModal: React.FC<LogoutModalProps> = ({ isOpen, onOpenClose, onLogout }) => {

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded-lg w-1/3 text-black">
        <h2 className="text-lg font-semibold mb-4">Logout</h2>
        <p>Are you sure you want to logout?</p>
        <div className="mt-4 flex justify-end">
          <button
            onClick={onOpenClose}
            className="mr-2 px-4 py-2 bg-deep-purple rounded border hover:border-black hover:border-1 focus:outline-none"
          >
            Close
          </button>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-indigo-500 text-white rounded border hover:border-black hover:border-1 focus:outline-none"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogoutModal;