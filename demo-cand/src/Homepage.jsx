import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import vuwImage from './assets/vuw.png';


const HomePage = () => {
  const navigate = useNavigate();

  const handleViewSwitch = () => {
    navigate('/candidate-overview');
  };

  return (
    <div className="homepage-container">
      <div className="home-view">
        <img src={vuwImage} alt="Victoria University of Wellington" className="home-image" />
        <h1 className="home-title">Web of Influence Database</h1>
        <button className="switch-button" onClick={handleViewSwitch}>Database Access</button>
      </div>
    </div>
  );
};

export default HomePage;
