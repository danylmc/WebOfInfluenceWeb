import React, { useState, useEffect } from 'react';

class Entry {
    constructor(people_id, party_id, electorate_id, total_expenses, total_donations, election_year) {
        this.people_id = people_id;
        this.party_id = party_id;
        this.electorate_id = electorate_id;
        this.total_expenses = total_expenses;
        this.total_donations = total_donations;
        this.election_year = election_year;
    }
}

const fetchAdditionalDetails = async (result) => {
    try {
        const personResponse = await fetch(`http://127.0.0.1:5000/candidates/search-id?people_id=${result.people_id}`);
        const personData = await personResponse.json();

        const partyResponse = await fetch(`http://127.0.0.1:5000/party/search-id?party_id=${result.party_id}`);
        const partyData = await partyResponse.json();

        const electorateResponse = await fetch(`http://127.0.0.1:5000/electorate/search-id?electorate_id=${result.electorate_id}`);
        const electorateData = await electorateResponse.json();

        return {
            firstName: personData[0]?.first_name || "Unknown",
            lastName: personData[0]?.last_name || "Unknown",
            party: partyData[0]?.party_name || "Unknown",
            electorate: electorateData?.electorate_name || "Unknown",
            total_expenses: result.total_expenses || 0,
            total_donations: result.total_donations || 0,
            election_year: result.election_year || "Unknown"
        };
    } catch (error) {
        console.error("Error fetching additional details:", error);
        return {
            firstName: "Error",
            lastName: "Error",
            party: "Error",
            electorate: "Error",
            total_expenses: result.total_expenses || 0,
            total_donations: result.total_donations || 0,
            election_year: result.election_year || "Unknown"
        };
    }
};

const Output = ({ results, onExportCSV }) => {
    const [processedResults, setProcessedResults] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [resultEntries, setResultEntries] = useState([]);

    useEffect(() => {
        const processResults = async () => {
            setIsLoading(true);

            if (!results || results.length === 0 || (results.length === 1 && typeof results[0] === 'string' && results[0] === 'No results found')) {
                setProcessedResults([]);
                setResultEntries([]);
                setIsLoading(false);
                return;
            }

            try {
                const detailedResults = await Promise.all(
                    results.map(result => fetchAdditionalDetails(result))
                );

                setProcessedResults(detailedResults);

                const entries = detailedResults.map(detail =>
                    new Entry(
                        detail.firstName,
                        detail.lastName,
                        detail.party,
                        detail.electorate,
                        detail.total_expenses,
                        detail.total_donations,
                        detail.election_year
                    )
                );
                setResultEntries(entries);

            } catch (error) {
                console.error("Error processing results:", error);
                setProcessedResults([]);
                setResultEntries([]);
            } finally {
                setIsLoading(false);
            }
        };

        processResults();
    }, [results]);

    if (isLoading) {
        return <div>Loading results...</div>;
    }

    if (processedResults.length === 0) {
        return <p className="text-center text-gray-500">No results found</p>;
    }

    return (
        <div>
            <div className="mb-4">
                <button 
                    onClick={() => onExportCSV(processedResults)}
                    className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                    Export to CSV
                </button>
            </div>
            
            <table className="w-full border-collapse">
                <thead>
                    <tr className="bg-gray-200">
                        <th className="border p-2">Name</th>
                        <th className="border p-2">Party</th>
                        <th className="border p-2">Electorate</th>
                        <th className="border p-2">Election Year</th>
                        <th className="border p-2">Total Expenses</th>
                        <th className="border p-2">Total Donations</th>
                    </tr>
                </thead>
                <tbody>
                    {processedResults.map((detail, index) => (
                        <tr key={index} className="hover:bg-gray-100">
                            <td className="border p-2">{detail.firstName} {detail.lastName}</td>
                            <td className="border p-2">{detail.party}</td>
                            <td className="border p-2">{detail.electorate}</td>
                            <td className="border p-2">{detail.election_year}</td>
                            <td className="border p-2">{detail.total_expenses}</td>
                            <td className="border p-2">{detail.total_donations}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Output;