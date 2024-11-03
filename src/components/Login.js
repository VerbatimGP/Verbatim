import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginSignup() {
  const [showLogin, setShowLogin] = useState(true);
  const [role, setRole] = useState('student');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();  // Initialize navigate

  const toggleForm = () => setShowLogin(!showLogin);

  const handleRoleChange = (event) => setRole(event.target.value);
  const handleEmailChange = (event) => setEmail(event.target.value);
  const handlePasswordChange = (event) => setPassword(event.target.value);
  const handleConfirmPasswordChange = (event) => setConfirmPassword(event.target.value);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (showLogin) {
      // Login logic here
      console.log(`Logging in as ${role} with email: ${email}`);
      if (role === 'faculty') {
        navigate('/faculty');  // Redirect to Faculty Dashboard
      } else {
        navigate('/student');  // Redirect to Student Dashboard
      }
    } else {
      // Signup logic here, check passwords match
      if (password === confirmPassword) {
        console.log(`Signing up as ${role} with email: ${email}`);
        if (role === 'faculty') {
          navigate('/faculty');  // Redirect to Faculty Dashboard
        } else {
          navigate('/student');  // Redirect to Student Dashboard
        }
      } else {
        alert("Passwords do not match!");
      }
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-blue-300">
      <div className="bg-white p-8 rounded-3xl w-80 shadow-lg ">
        <h2 className="text-2xl font-bold mb-6 text-center">{showLogin ? "Login" : "Sign Up"}</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2"><b>I am a</b></label>
            <select
              value={role}
              onChange={handleRoleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="student">Student</option>
              <option value="faculty">Faculty</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={handleEmailChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={handlePasswordChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          {!showLogin && (
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2">Confirm Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                className="w-full p-2 border border-gray-300 rounded"
                required
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mb-4"
          >
            {showLogin ? "Login" : "Sign Up"}
          </button>
        </form>
        <p className="text-center">
          {showLogin ? "Don't have an account?" : "Already have an account?"}
          <button onClick={toggleForm} className="text-blue-500 ml-1">
            {showLogin ? "Sign Up" : "Login"}
          </button>
        </p>
      </div>
    </div>
  );
}

export default LoginSignup;
