//import React, {useRef, useEffect, useState} from 'react';
//import { Bar } from 'react-chartjs-2';  // Import Bar chart from react-chartjs-2
//import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

//const BarChart = () => {
  //const dataMap = new Map();

  //async function fetchData() {
    //const response = await fetch(`http://127.0.0.1:5000/candidates`);
    //const response2 = await fetch(`http://127.0.0.1:5000/party`);
    //if (!response.ok){
      //throw new Error("Error: couldn't get the data")
    //}
    //const result = await response.json();
    //const result2 = await response2.json();
    //console.log(response);
    //console.log(result);
    //console.log(response2);
    //console.log(result2);
    //loadData(result);
  //};

  //const loadData = (result) => {
    //esult.forEach(async (candidate) => {
      // const response = await fetch(`http://127.0.0.1:5000/candidates/search-id?people_id=${candidate.id}`);
      // const data = await response.json();
      // console.log(data);
      // dataMap.set(candidate);
    //});
    //console.log(data);
  //};

  //useEffect(() => {
    //fetchData();
  //}, []);

      //return (
        //<div></div>
      //);
    //};
    
    //export default BarChart;    

import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2'; 
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register the necessary Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BarChart = ({ results }) => {
  const [chartData, setChartData] = useState(null);

  // FUnction to fetch candidate names by people_id
  const fetchCandidateNames = async (people_id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/candidates/search-id?people_id=${people_id}`);
      const data = await response.json();
      return data[0]?.first_name + ' ' + data[0]?.last_name || 'Unknown';
    } catch (error) {
      console.error('Error fetching candidate name:', error);
      return 'Unknown';
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      if (results && results.length > 0) {
        // Fetch names for each candidate based on people_id
        const labels = await Promise.all(
          results.map(async (result) => await fetchCandidateNames(result.people_id))
        );

        const donations = results.map(result => result.total_donations);

        setChartData({
          labels: labels,
          datasets: [
            {
              label: 'Total Donations',
              data: donations,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        });
      }
    };
      //if (results.length > 0 && results !== 'No results found') {
          // Prepare data for the chart
          //const labels = results.map(result => `${result.firstName} ${result.lastName}`);
          //const donations = results.map(result => result.total_donations);

          //setChartData({
              //labels: labels,
              //datasets: [
                  //{
                      //label: 'Total Donations',
                      //data: donations,
                      ////backgroundColor: 'rgba(75, 192, 192, 0.6)', 
                      //borderColor: 'rgba(75, 192, 192, 1)',
                      //borderWidth: 1,
                  //},
              //],
          //});
      //}
    //};

    fetchData();
  }, [results]);

  // If no results or chart data is available
  if (!chartData) {
      return <p>No data to display</p>;
  }

  // Chart.js options 
  const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
          title: {
              display: true,
              text: 'Total Donations per Candidate',
              font: { size: 18 },
          },
          tooltip: {
              callbacks: {
                  label: function (tooltipItem) {
                      return `Total Donations: $${tooltipItem.raw.toLocaleString()}`;
                  },
              },
          },
      },
      scales: {
          x: {
              title: {
                  display: true,
                  text: 'Candidates',
              },
              ticks: {
                 autoSkip: false,
                  maxRotation: 90,
                  minRotation: 45,
              },
          },
          y: {
              title: {
                  display: true,
                  text: 'Donations ($)',
              },
              beginAtZero: true,
              ticks: {
                  callback: function (value) {
                      return `$${value.toLocaleString()}`;
                  },
              },
          },
      },
  };

  return (
      <div className="chart-container w-full">
          <Bar data={chartData} options={options} />
      </div>
  );
};

export default BarChart;