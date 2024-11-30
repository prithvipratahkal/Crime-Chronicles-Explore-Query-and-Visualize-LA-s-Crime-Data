import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function ChartComponent({ chartData, chartType }) {
    
const getChartOptions = () => {
    const animationSettings = {
      duration: 1000, // Duration for transitions
      easing: 'easeInOutQuad', // Smooth easing
    };

    return {
      chart: {
        type: chartType, // Use chartType directly
        animation: animationSettings, // Add animation settings
      },
      title: {
        text: chartData.title, // Title from chartData
      },
      xAxis: chartType !== 'pie' ? { // Only for non-pie charts
        categories: chartData.labels,
      } : undefined,
      yAxis: chartType !== 'pie' ? { // Only for non-pie charts
        title: {
          text: 'Crime Count',
        },
      } : undefined,
      series: [{
        name: chartType === 'pie' ? 'Crime Type' : 'Crime Count', // Series name changes based on chartType
        data: chartType === 'pie'
          ? chartData.labels.map((label, index) => ({
              name: label,
              y: chartData.datasets[0].data[index],
            }))
          : chartData.datasets[0].data, // For bar/line, use raw data
        animation: animationSettings, // Series-specific animation
      }],
    };
  };


  return (
    <div style={{
        width: '80%',
        marginInline: 'auto',
        borderRadius: '15px',
        overflow: 'hidden',
        border: 'solid 2px #272626', 
        padding: '1rem',
    }}>
      <HighchartsReact
        highcharts={Highcharts}
        options={getChartOptions(chartType)} // Pass the options dynamically based on the selected chart type
      />
    </div>
  );
}

export default ChartComponent;
