import React from 'react';
import '../styles/FilterOptions.css';

function FilterOptions({ onFilterChange }) {
  return (
    <div className="filter-options">
      <label>
        <input
          type="radio"
          name="filter"
          value="crimeType"
          onChange={onFilterChange}
        />
        Crime Type
      </label>
      <label>
        <input
          type="radio"
          name="filter"
          value="timeRange"
          onChange={onFilterChange}
        />
        Time Range
      </label>
    </div>
  );
}

export default FilterOptions;
