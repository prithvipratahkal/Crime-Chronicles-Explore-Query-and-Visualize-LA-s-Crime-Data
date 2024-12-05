import React from 'react';
// import { Pie } from 'react-chartjs-2';
import ChartComponent from './ChartComponent'


// Import the CSS file
import '../styles/Visualization.css';

function Visualization({ chartType, viewType }) { // just for sample output!
  const chartData = {
    title: 'Crime Distribution by Type',
    labels: ['Theft', 'Assault', 'Burglary', 'Vandalism', 'Robbery'],
    datasets: [
      {
        data: [120, 45, 67, 34, 78],
        // backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
      },
    ],
  };

  if (viewType === 'text') {
    return (
      <div className="text-container">
        <h3>Response</h3>
        <textarea
          placeholder="AI-generated response will appear here..."
          readOnly
          value="Sample Text Output: Theft is the most reported crime in 2022."
        />
      </div>
    );
  }

  // return (
  //   <div className="visualization-container">
  //     <h3 className="visualization-title">Visualization</h3>
  //     <div className="chart-container">
  //       <Pie data={chartData} options={{ maintainAspectRatio: false }} />
  //     </div>
  //   </div>
  // );
  
  return (
    <div>
      {/* Send chartData and chartType to the ChartComponent */}
      <ChartComponent chartData={chartData} chartType={chartType} />
    </div>
  );

}

export default Visualization;
