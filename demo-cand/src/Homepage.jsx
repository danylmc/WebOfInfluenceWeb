import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './auth/AuthProvider';
import './HomePage.css';


const HomePage = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const navigate = useNavigate();
  const { logout } = useAuth();

  //Handld logout functionality
  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login', { replace: true });
    } catch (e) {
      console.error(e);
      alert('Failed to log out, please try again.');
    }
  };

  return (
    <div className="container">
      {/* Top bar with logout button */}
      <div className="top-bar">
        <h1 className="title">Web of Influence Research Homepage</h1>
        <div style={{ display: 'flex', gap: 8 }}>
          <Link to="/settings" className="button">Settings</Link>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
      </div>

      <div className="main-options">
        <Link to="/candidate-overview" className="button">
          Donations Overview
        </Link>

        <Link to="/meetings" className="button">
          Ministerial Meetings
        </Link>
      </div>

      <div className="about-section">
        <h2 className="about-title">Current Status</h2>
        <p className="about-description">
          This website provides access to information about political donations and ministerial diaries in New Zealand. 
        </p>
        <p className="about-description">
          You can search through election donation data (both individual and overview) for election years 2011, '14, '17 and 2023, and access detailed records of ministerial diaries.
        </p>
      </div>

      {/* 
      <div className="search-section">
        <input
          type="text"
          placeholder="Enter First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className="search-input"
        />
        <input
          type="text"
          placeholder="Enter Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          className="search-input"
        />
        <button onClick={handleSearchSubmit} className="search-button">
          Search Profile
        </button>
      </div> */}
    </div>
  );
};

export default HomePage;
