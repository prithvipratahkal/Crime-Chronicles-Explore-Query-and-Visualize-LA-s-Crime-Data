import React from 'react';
import '../styles/FilterOptions.css';


function ChartTypeSelector({ setChartType }) {
  return (
    <div className="chart-type-selector" >
      <strong><span>Chart Type:</span></strong>
      <label>
        <input
          type="radio"
          name="chartType"
          value="pie"
          defaultChecked
          onChange={(e) => setChartType(e.target.value)}
        />
        <span>Pie Chart</span>
        
      </label>
      <label>
        <input
          type="radio"
          name="chartType"
          value="bar"
          onChange={(e) => setChartType(e.target.value)}
        />
        <span>Bar Chart</span>
      </label>
      <label>
        <input
          type="radio"
          name="chartType"
          value="line"
          onChange={(e) => setChartType(e.target.value)}
        />
        <span>Line</span>
      </label>
    </div>
    
  );
}

export default ChartTypeSelector;

