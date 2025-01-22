import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Homepage.jsx'; 
import App from './App.jsx'; 

createRoot(document.getElementById('root')).render(
  <Router>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/candidate-overview" element={<App />} />
    </Routes>
  </Router>
);
