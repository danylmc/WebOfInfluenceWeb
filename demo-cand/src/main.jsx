import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// pages
import HomePage from './Homepage'; 
import CandidateOverview from './CandidateOverview.jsx';
import MeetingsSearch from './MeetingsSearch.jsx';
import PersonProfile from './PersonProfile.jsx';
import LoginPage from './Loginpage.jsx'; 

// auth
import AuthProvider from './auth/AuthProvider';
import ProtectedRoute from './auth/ProtectedRoute';

createRoot(document.getElementById('root')).render(
  <AuthProvider>
    <Router basename="/WebOfInfluenceResearch">
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        
        {/* Protected routes - all pages require authentication */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/candidate-overview" element={<CandidateOverview />} />
          <Route path="/meetings" element={<MeetingsSearch />} />
          <Route path="/person/:firstName/:lastName" element={<PersonProfile />} />
        </Route>
      </Routes>
    </Router>
  </AuthProvider>
);
