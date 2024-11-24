import React, { useState } from 'react';
import '../styles/QueryInput.css';

function QueryInput({ setViewType }) {
  const [query, setQuery] = useState('');

  const handleDropdownChange = (e) => {
    setViewType(e.target.value); // Pass the selected value (Chart/Text) to the parent
  };


  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // Prevent the default form submission
    }
  };
  
  return (
    <div className="query-input">
      <input
        type="text"
        placeholder="Type your crime data query here..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleInputKeyDown} // Add this handler
      />
      <select onChange={handleDropdownChange}>
        <option value="chart">Chart</option>
        <option value="text">Text</option>
      </select>
    </div>
  );
  


}

export default QueryInput;
