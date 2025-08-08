import React, { useState } from 'react';
import Output from './Output.jsx';
import { useNavigate } from 'react-router-dom';
import BarChart from './BarChart.jsx';
import { API_BASE } from './apiConfig';
import './CandidateOverview.css';

function CandidateOverview() {
    // State variables for search query
    const [searchQuery, setSearchQuery] = useState({
        firstName: '',
        lastName: '',
        party: '',
        electorate: '',
    });

    // State to manage selected years for filtering
    const [selectedYears, setSelectedYears] = useState({
        2023: true,
        2017: false,
        2014: false,
        2011: false
    });

    // State to manage results and processed results
    const [results, setResults] = useState(null);
    const [processedResults, setProcessedResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [hasSearched, setHasSearched] = useState(false);

    const navigate = useNavigate();
    const handleBackToHome = () => navigate('/home');

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
        setHasSearched(true);
        setError(null);
        setIsLoading(true);
        // Reset results and processed results
        setResults([]);
        setProcessedResults(null);

        // Filter selected years
        const activeYears = Object.keys(selectedYears).filter(year => selectedYears[year]);

        // Check if at least one year is selected and if there are search criteria
        const hasCriteria = !!(
            searchQuery.firstName ||
            searchQuery.lastName ||
            searchQuery.party ||
            searchQuery.electorate
        );

        if (activeYears.length === 0 || !hasCriteria) {
            setIsLoading(false);
            setResults([]);
            setError('Pick at least one year and enter a filter.');
            return;
        }

        // Prepare search parameters
        const params = new URLSearchParams();
        if (searchQuery.firstName) params.append('first_name', searchQuery.firstName);
        if (searchQuery.lastName) params.append('last_name', searchQuery.lastName);
        if (searchQuery.party) params.append('party_name', searchQuery.party);
        if (searchQuery.electorate) params.append('electorate_name', searchQuery.electorate);

        let allResults = [];

        for (let year of activeYears) {
            try {
                const response = await fetch(
                    `${API_BASE}/candidates/election-overview/${year}/search/combined?${params.toString()}`
                );

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    const resultsWithYear = data.map(item => ({
                        ...item,
                        election_year: year,
                    }));
                    allResults = [...allResults, ...resultsWithYear];
                }
            } catch (err) {
                console.error(`Error fetching data for ${year}:`, err);
            }
        }

        // Process results for the chart
        setResults(allResults.length === 0 ? [] : allResults);
        setIsLoading(false);
    };

    const handleExportCSV = (processedResults) => {
        if (!processedResults || processedResults.length === 0) {
            alert('No data to export');
            return;
        }

        const defaultName = 'election_candidates';
        const filename = prompt('Enter a name for your CSV file:', defaultName) || defaultName;

        const finalFilename = filename.endsWith('.csv') ? filename : `${filename}.csv`;

        const headers = ['Name', 'Party', 'Electorate', 'Election Year', 'Total Expenses', 'Total Donations'];

        const csvRows = [
            headers.join(','),
            ...processedResults.map(row => [
                `${row.firstName} ${row.lastName}`,
                row.party,
                row.electorate,
                row.election_year,
                row.total_expenses,
                row.total_donations
            ].join(','))
        ];

        const csvContent = csvRows.join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', finalFilename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Processed results and setProcessedResults
    const processedResultsForChart = (results) => {
        if (results && results.length > 0 ) {
            const processedData = results.map(result => ({
                firstName: result.firstName || 'Unknown',
                lastName: result.lastName || 'Unknown', 
                total_donations: result.total_donations || 0,
            }));
            setProcessedResults(processedData);
        }
    };

    return (
        <div className="page-wrapper">
            <div className="candidate-wrapper">
                <div className="candidate-inner">
                    <div className="header-row">
                        <h2>Filter by Year</h2>
                        <button onClick={handleBackToHome}> 
                            ←  Back to Home</button>
                    </div>

                    {/* Year Toggle */}
                    <div className="year-toggle-group">
                    {Object.keys(selectedYears).sort().map((year) => (
                        <button
                        key={year}
                        type="button"
                        className={`year-chip ${selectedYears[year] ? 'active' : ''}`}
                        onClick={() => handleYearChange(year)}
                        aria-pressed={selectedYears[year]}
                        >
                        {year}
                        </button>
                    ))}
                    </div>

                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', margin: '1.5rem 0 0.5rem' }}>
                        Search Filters
                    </h3>

                    <input
                        type="text"
                        name="firstName"
                        placeholder="First Name"
                        value={searchQuery.firstName}
                        onChange={handleSearchChange}
                    />
                    <input
                        type="text"
                        name="lastName"
                        placeholder="Last Name"
                        value={searchQuery.lastName}
                        onChange={handleSearchChange}
                    />
                    <input
                        type="text"
                        name="party"
                        placeholder="Party"
                        value={searchQuery.party}
                        onChange={handleSearchChange}
                    />
                    <input
                        type="text"
                        name="electorate"
                        placeholder="Electorate"
                        value={searchQuery.electorate}
                        onChange={handleSearchChange}
                    />

                    <button onClick={handleSearchSubmit} className="search-button">
                        Search
                    </button>
                </div>
            </div>

            {hasSearched && (
            <div className="results-section">
                <h2>Election Candidates Overview Database Search & Filter</h2>

                {error && <div className="error">{error}</div>}
                {isLoading && <div>Loading results...</div>}

                {Array.isArray(results) && results.length > 0 && (
                <Output results={results} onExportCSV={handleExportCSV} />
                )}

                <BarChart results={results} isLoading={isLoading} />
            </div>
            )}
        </div>
        );

}

export default CandidateOverview;