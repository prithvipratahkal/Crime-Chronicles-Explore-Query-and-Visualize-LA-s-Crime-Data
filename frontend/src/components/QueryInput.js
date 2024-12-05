import React, { useState } from 'react';
import '../styles/QueryInput.css';

function QueryInput({ setViewType }) {
  const [query, setQuery] = useState('');

  const handleDropdownChange = (e) => {
    setViewType(e.target.value); // Pass the selected value (Chart/Text) to the parent
  };


  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      if (query.trim() !== '') {
        e.preventDefault(); // Prevent the default form submission
        console.log("query entered by user: ", {query});
        // setQuery(''); // Clear the input field
      }
    }
  };

  const handleSubmit = () => {
    if (query.trim() !== '') {
      console.log("query entered by user: ", {query});
      // setQuery(''); // Clear the input field
    }
  };
  
  return (
    <div className="query-input">
      <select onChange={handleDropdownChange}>
        <option value="chart">Chart</option>
        <option value="text">Text</option>
      </select>

      <input
        type="text"
        placeholder="Type your crime data query here..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleInputKeyDown} // Add this handler
      />
      
      <button onClick={handleSubmit}>Go</button> {/* Submit button */}
      
    </div>
  );
  


}

export default QueryInput;
