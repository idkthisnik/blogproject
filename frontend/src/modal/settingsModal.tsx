import React, { useState, useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: any) => Promise<boolean> | undefined;
  option: string;
  errorMessage: string
  setErrorMessage: (error: string) => void;
}

const SettingsModal: React.FC<ModalProps> = ({ isOpen, onClose, onSubmit, option, errorMessage, setErrorMessage}) => {
  const [formData, setFormData] = useState<any>({});
  const [isSuccess, setIsSuccess] = useState<boolean>();
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      setIsSuccess(undefined); 
      setShowPassword(false)
    }
  }, [isOpen]);
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData: any) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitted(true)

    const result = await onSubmit(formData); 
    if (typeof result === 'boolean') {
      setIsSuccess(result);
      setFormData({})
    }  
  }

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded-lg w-1/3">
        <h2 className="text-lg font-semibold mb-4">Enter {option} details</h2>
        <form onSubmit={handleSubmit}>
          {option === 'change login' && (
            <div>
              <input
                type="text"
                name="login"
                placeholder="Login"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type="text"
                name="newLogin"
                placeholder="New Login"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-blue-500 hover:underline"
              >
                {showPassword ? "Hide Passwords" : "Show Passwords"}
              </button>
            </div>
          )}
          {option === 'change password' && (
            <div>
              <input
                type="text"
                name="login"
                placeholder="Login"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type={showPassword ? "text" : "password"}
                name="newPassword"
                placeholder="New Password"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-blue-500 hover:underline"
              >
                {showPassword ? "Hide Passwords" : "Show Passwords"}
              </button>
            </div>
        )}
          {option === 'change email' && (
            <div>
              <input
                type="text"
                name="login"
                placeholder="Login"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type="email"
                name="newEmail"
                placeholder="New Email"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-blue-500 hover:underline"
              >
                {showPassword ? "Hide Passwords" : "Show Passwords"}
              </button>
            </div>
          )}
          {option === 'delete account' && (
            <div>
              <input
                type="text"
                name="login"
                placeholder="Login"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                onChange={handleInputChange}
                className="w-full mb-2 p-2 border rounded"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-blue-500 hover:underline"
              >
                {showPassword ? "Hide Passwords" : "Show Passwords"}
              </button>
            </div>
          )}
          <div className="flex justify-between">
            <button type="submit" className="border rounded-full px-2 border-indigo-500 p-2 bg-indigo-500 text-white mt-2 hover:border-black hover:border-1">Submit</button>
              <div>
                {isSubmitted && isSuccess ? (
                  <p className="text-green-500">Success!</p>
                ) : isSubmitted && isSuccess === false ? (
                  <p className="text-red-500">{errorMessage}</p>
                ) : null}
              </div>
            <button onClick={onClose} className="border rounded-full px-2 border-deep-purple p-2 bg-deep-purple text-white mt-2 hover:border-black hover:border-1">Close</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsModal;