import React, { useState } from 'react';
import MeetingsTable from './MeetingsTable';
import './MeetingsSearch.css';
import { API_BASE } from './apiConfig';
import { useNavigate } from 'react-router-dom';


const MeetingsSearch = () => {
  const [searchQuery, setSearchQuery] = useState({
    firstName: '',
    lastName: '',
    startDate: '',
    endDate: '',
    portfolio: ''
  });
  const [meetings, setMeetings] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  
  const handleSearchChange = (event) => {
    const { name, value } = event.target;
    setSearchQuery(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSearchSubmit = async () => {
    if (!searchQuery.firstName && !searchQuery.lastName && !searchQuery.startDate && !searchQuery.endDate && !searchQuery.portfolio) {
      alert('Please enter at least one search criteria');
      return;
    }

    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        first_name: searchQuery.firstName,
        last_name: searchQuery.lastName,
        start_date: searchQuery.startDate,
        end_date: searchQuery.endDate,
        portfolio: searchQuery.portfolio
      });

      const response = await fetch(
        `${API_BASE}/ministerial_diaries/search-cand-filter?${params.toString()}`
      );

      if (response.ok) {
        const data = await response.json();
        setMeetings(data);
      } else {
        const error = await response.json();
        alert(error.error || 'No meetings found');
        setMeetings([]);
      }
    } catch (error) {
      console.error('Error fetching meetings:', error);
      alert('Error fetching meetings data');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 relative">
      {/* Header row with title and Back button */}
      <div className="header-row">
        <h2 className="text-2xl font-bold">Search Ministerial Meetings</h2>
        <button
          onClick={() => navigate('/')}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow"
        >
          ← Back to Home
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4 max-w-2xl mt-6 mb-4">
        <input
          type="text"
          name="firstName"
          placeholder="First Name"
          value={searchQuery.firstName}
          onChange={handleSearchChange}
          className="p-2 border rounded"
        />
        <input
          type="text"
          name="lastName"
          placeholder="Last Name"
          value={searchQuery.lastName}
          onChange={handleSearchChange}
          className="p-2 border rounded"
        />
        <input
          type="date"
          name="startDate"
          placeholder="Start Date"
          value={searchQuery.startDate}
          onChange={handleSearchChange}
          className="p-2 border rounded"
        />
        <input
          type="date"
          name="endDate"
          placeholder="End Date"
          value={searchQuery.endDate}
          onChange={handleSearchChange}
          className="p-2 border rounded"
        />
        <input
          type="text"
          name="portfolio"
          placeholder="Portfolio"
          value={searchQuery.portfolio}
          onChange={handleSearchChange}
          className="p-2 border rounded"
        />
      </div>
      <button
        onClick={handleSearchSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        disabled={isLoading}
      >
        {isLoading ? 'Searching...' : 'Search Meetings'}
      </button>

      {meetings.length > 0 && <MeetingsTable meetings={meetings} />}
    </div>
  );
};

export default MeetingsSearch;
