import React, { useState } from 'react';
import './style.css';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import FilterOptions from './components/FilterOptions';
import Visualization from './components/Visualization';
import ChartTypeSelector from './components/ChartTypeSelector';
import './styles/App.css';

function App() {
  const [chartType, setChartType] = useState('pie'); // Default chart type
  const [viewType, setViewType] = useState('chart'); // Default view type
  const [filter, setFilter] = useState('crimeType'); // Default filter

  // Handle filter changes
  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  // Handle view type changes (chart or text)
  const handleViewTypeChange = (viewType) => {
    setViewType(viewType); // Correctly update the view type
  };

  return (
    <div className="container">
      <Header />
      <QueryInput setViewType={handleViewTypeChange} />
      <FilterOptions onFilterChange={handleFilterChange} />
      <Visualization chartType={chartType} viewType={viewType} />
      {viewType === 'chart' && <ChartTypeSelector setChartType={setChartType} />}
    </div>
  );
}

export default App;
