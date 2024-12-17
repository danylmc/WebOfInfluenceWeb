import React from 'react';

const SearchForm = ({ searchQuery, onSearchChange, onSearchSubmit }) => {
    return (
        <div>
            <label>
                First Name:
                <input
                    type="text"
                    name="firstName"
                    value={searchQuery.firstName}
                    onChange={onSearchChange}
                />
            </label>
            <label>
                Last Name:
                <input
                    type="text"
                    name="lastName"
                    value={searchQuery.lastName}
                    onChange={onSearchChange}
                />
            </label>
            <label>
                Party:
                <input
                    type="text"
                    name="party"
                    value={searchQuery.party}
                    onChange={onSearchChange}
                />
            </label>
            <label>
                Electorate:
                <input
                    type="text"
                    name="electorate"
                    value={searchQuery.electorate}
                    onChange={onSearchChange}
                />
            </label>

            <div>
                <button onClick={() => onSearchSubmit('candidate')}>Search by Candidate</button>
                <button onClick={() => onSearchSubmit('party')}>Search by Party</button>
                <button onClick={() => onSearchSubmit('electorate')}>Search by Electorate</button>
            </div>
        </div>
    );
};

export default SearchForm;
