// App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './Navigation';
import HomePage from './Homepage';
import CandidateOverview from './CandidateOverview'; 
import MeetingsSearch from './MeetingsSearch';
import PersonProfile from './PersonProfile';

import ProtectedRoute from './auth/ProtectedRoute';
import Login from './pages/Login';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      <main className="container mx-auto py-6">
        <Routes>
          {/* public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/home" element={<HomePage />} />

          {/* protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/candidate-overview" element={<CandidateOverview />} />
            <Route path="/meetings" element={<MeetingsSearch />} />
            <Route path="/person/:firstName/:lastName" element={<PersonProfile />} />
          </Route>
        </Routes>
      </main>
    </div>
  );
};

export default App;
