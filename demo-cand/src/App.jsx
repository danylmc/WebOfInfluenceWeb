import React, { useState } from 'react';
import Output from './Output.jsx';

function App() {
    const [searchQuery, setSearchQuery] = useState({
        firstName: '',
        lastName: '',
        party: '',
        electorate: '',
    });
    const [selectedYears, setSelectedYears] = useState({
        2023: true,
        2017: false,
        2014: false,
        2011: false
    });
    const [results, setResults] = useState([]);

    const handleSearchChange = (event) => {
        const { name, value } = event.target;
        setSearchQuery(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleYearChange = (year) => {
        setSelectedYears(prevYears => ({
            ...prevYears,
            [year]: !prevYears[year]
        }));
    };
    const handleSearchSubmit = async () => {
        const activeYears = Object.keys(selectedYears).filter(year => selectedYears[year]);
    
        // If no active years are selected, return no results
        if (activeYears.length === 0) {
            setResults(['No results found']);
            return;
        }
    
        // Check if any search criteria are provided
        const hasCriteria =
            searchQuery.firstName ||
            searchQuery.lastName ||
            searchQuery.party ||
            searchQuery.electorate;
    
        let allResults = [];
    
        // Fetch results based on criteria
        if (hasCriteria) {
            for (let year of activeYears) {
                const searchUrls = [
                    searchQuery.firstName || searchQuery.lastName
                        ? `http://127.0.0.1:5000/candidates/election-overview/${year}/search/name?first_name=${searchQuery.firstName}&last_name=${searchQuery.lastName}`
                        : null,
                    searchQuery.party
                        ? `http://127.0.0.1:5000/candidates/election-overview/${year}/search/party?party_name=${searchQuery.party}`
                        : null,
                    searchQuery.electorate
                        ? `http://127.0.0.1:5000/candidates/election-overview/${year}/search/electorate?electorate_name=${searchQuery.electorate}`
                        : null,
                ].filter(url => url !== null);
    
                for (let url of searchUrls) {
                    try {
                        const response = await fetch(url);
                        const data = await response.json();
    
                        const resultsWithYear = data.map(item => ({
                            ...item,
                            election_year: year,
                        }));
    
                        allResults = [...allResults, ...resultsWithYear];
                    } catch (err) {
                        console.error(`Error fetching data for ${year}:`, err);
                    }
                }
            }
        }
    
        // If no criteria and no specific search results, show "No results found"
        if (!hasCriteria || allResults.length === 0) {
            setResults(['No results found']);
        } else {
            setResults(allResults);
        }
    };

    return (
        <div className="flex">
            {/* Sidebar for Year and Search Filters */}
            <div className="w-64 p-4 bg-gray-100 h-screen">
                <h2 className="text-xl font-bold mb-4">Filter by Year</h2>
                {Object.keys(selectedYears).map(year => (
                    <div key={year} className="mb-2">
                        <label className="inline-flex items-center">
                            <input
                                type="checkbox"
                                checked={selectedYears[year]}
                                onChange={() => handleYearChange(year)}
                                className="form-checkbox"
                            />
                            <span className="ml-2">{year}</span>
                        </label>
                    </div>
                ))}

                <div className="mt-6">
                    <h3 className="text-lg font-semibold mb-2">Search Filters</h3>
                    <input
                        type="text"
                        name="firstName"
                        placeholder="First Name"
                        value={searchQuery.firstName}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="lastName"
                        placeholder="Last Name"
                        value={searchQuery.lastName}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="party"
                        placeholder="Party"
                        value={searchQuery.party}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="electorate"
                        placeholder="Electorate"
                        value={searchQuery.electorate}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                </div>

                <div className="mt-4">
                    <button 
                        onClick={handleSearchSubmit}
                        className="w-full bg-blue-500 text-white p-2 rounded"
                    >
                        Search
                    </button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 p-4">
                <h1 className="text-2xl font-bold mb-4">Election Candidates Database</h1>
                
                <Output results={results} />
            </div>
        </div>
    );
}

export default App;