import React, { useState, useEffect } from 'react';

const fetchDetails = async (result) => {
    if (!result.people_id || !result.party_id || !result.electorate_id) {
        return { 
            firstName: "Missing ID", 
            lastName: "Missing ID", 
            party: "Missing ID", 
            electorate: "Missing ID",
            total_expenses: "Missing ID",
            total_donations: "Missing ID"
        };
    }

    const urls = {
        name: `http://127.0.0.1:5000/candidates/search-id?people_id=${result.people_id}`,
        party: `http://127.0.0.1:5000/party/search-id?party_id=${result.party_id}`,
        electorate: `http://127.0.0.1:5000/electorate/search-id?electorate_id=${result.electorate_id}`,
    };

    try {
        const responses = await Promise.all(
            Object.values(urls).map((url) =>
                fetch(url).then((res) => {
                    if (!res.ok) {
                        console.error(`Error fetching URL: ${url}, Status: ${res.status}`);
                        throw new Error("API request failed");
                    }
                    return res.json();
                })
            )
        );

        console.log("API responses:", responses);

        return {
            firstName:responses[0][0].first_name || "Unknown First Name",
            lastName: responses[0][0].last_name || "Unknown Last Name",
            party: responses[1][0].party_name || "Unknown Party",
            electorate: responses[2]?.electorate_name || "Unknown Electorate",
            total_expenses: result.total_expenses == 0?  0.00 : result.total_expenses || "Unknown Total Expenses",
            total_donations: result.total_donations == 0? 0.00 : result.total_donations || "Unknown Total Donations"
        };
    } catch (error) {
        console.error("Error fetching details:", error);
        return { 
            firstName: "Error", 
            lastName: "Error", 
            party: "Error", 
            electorate: "Error" 
        };
    }
};

// Output Component
const Output = ({ results }) => {
    const [detailedResults, setDetailedResults] = useState([]);

    useEffect(() => {
        // Fetch details for all results
        const fetchAllDetails = async () => {
            const details = await Promise.all(results.map(fetchDetails));
            setDetailedResults(details);
        };

        fetchAllDetails();
    }, [results]);

    return (
        <div>
            <div>
            {detailedResults.length > 0 ? (
                <table border="1">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Party</th>
                            <th>Electorate</th>
                            <th>Total Expenses</th>
                            <th>Total Donations</th>
                        </tr>
                    </thead>
                    <tbody>
                        {detailedResults.map((detail, index) => (
                            <tr key={index}>
                                <td>{detail.firstName} {detail.lastName}</td>
                                <td>{detail.party}</td>
                                <td>{detail.electorate}</td>
                                <td>{detail.total_expenses}</td>
                                <td>{detail.total_donations}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No results found</p>
            )}
        </div>
        </div>
    );
};

export default Output;