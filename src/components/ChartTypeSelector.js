import React from 'react';

function ChartTypeSelector({ setChartType }) {
  return (

  <div style={{margin:'15px'}}>        
    <div style={{ marginTop: '20px' }}>
      <span>Chart Type:</span>
      <label style={{ marginLeft: '10px' }}>
        <input
          type="radio"
          name="chartType"
          value="pie"
          defaultChecked
          onChange={(e) => setChartType(e.target.value)}
        />
        Pie Chart
      </label>
      <label style={{ marginLeft: '10px' }}>
        <input
          type="radio"
          name="chartType"
          value="bar"
          onChange={(e) => setChartType(e.target.value)}
        />
        Bar Chart
      </label>
      <label style={{ marginLeft: '10px' }}>
        <input
          type="radio"
          name="chartType"
          value="heatmap"
          onChange={(e) => setChartType(e.target.value)}
        />
        Heatmap
      </label>
    </div>
    </div>
    
  );
}

export default ChartTypeSelector;

