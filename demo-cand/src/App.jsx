import React, { useState } from 'react';
import Output from './Output.jsx';

function App() {
    const [searchQuery, setSearchQuery] = useState({
        firstName: '',
        lastName: '',
        party: '',
        electorate: '',
    });
    const [category, setCategory] = useState('');
    const [results, setResults] = useState([]);

    const handleSearchChange = (event) => {
        const { name, value } = event.target;
        setSearchQuery(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSearchSubmit = async (searchCategory) => {
        setCategory(searchCategory);
        const query = searchQuery[searchCategory];
        let url = '';
        if (searchCategory === 'candidate') {
            url = `http://127.0.0.1:5000/candidates/election-overview/2023/search/name?first_name=${searchQuery.firstName}&last_name=${searchQuery.lastName}`;
        } else if (searchCategory === 'party') {
            url = `http://127.0.0.1:5000/candidates/election-overview/2023/search/party?party_name=${searchQuery.party}`;
        } else if (searchCategory === 'electorate') {
            url = `http://127.0.0.1:5000/candidates/election-overview/2023/search/electorate?electorate_name=${searchQuery.electorate}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();
            setResults(data.error ? [data.error] : data);
        } catch (err) {
            setResults(['Error fetching data']);
        }
    };

    return (
        <div>
            <h1>2023 Donations Database</h1>

            <div>
                <label>
                    First Name:
                    <input
                        type="text"
                        name="firstName"
                        value={searchQuery.firstName}
                        onChange={handleSearchChange}
                    />
                </label>
                <label>
                    Last Name:
                    <input
                        type="text"
                        name="lastName"
                        value={searchQuery.lastName}
                        onChange={handleSearchChange}
                    />
                </label>
                <label>
                    Party:
                    <input
                        type="text"
                        name="party"
                        value={searchQuery.party}
                        onChange={handleSearchChange}
                    />
                </label>
                <label>
                    Electorate:
                    <input
                        type="text"
                        name="electorate"
                        value={searchQuery.electorate}
                        onChange={handleSearchChange}
                    />
                </label>

                <div>
                    <button onClick={() => handleSearchSubmit('candidate')}>Search by Candidate</button>
                    <button onClick={() => handleSearchSubmit('party')}>Search by Party</button>
                    <button onClick={() => handleSearchSubmit('electorate')}>Search by Electorate</button>
                </div>
            </div>

            {category && <Output results={results} />}
        </div>
    );
}

export default App;
