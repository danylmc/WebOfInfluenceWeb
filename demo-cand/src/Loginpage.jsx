import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from './auth/AuthProvider';
import './LoginPage.css';

const LoginPage = () => {
  // Use the auth context to handle login
  const { loginEmail, loginGoogle } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Handle login with email and password
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/home';

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await loginEmail(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
    }
  };

  /* Hardcoded login for demonstration purposes */
  /* const handleLogin = (e) => {
    e.preventDefault();

    if (username.trim() === 'admin' && password === 'password') {
      navigate('/home'); // Redirect to dashboard or home page
    } else {
      alert('Invalid login. Please try again.');
    }
  }; */

  return (
    <div className="login-container">
      <h1 className="login-title">Web of Influence Research</h1>

      {/* email/password login form */}
      <form onSubmit={handleEmailLogin} className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="login-input"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="login-input"
          required
        />
        <button type="submit" className="login-button">Login</button>
      </form>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
};

export default LoginPage;