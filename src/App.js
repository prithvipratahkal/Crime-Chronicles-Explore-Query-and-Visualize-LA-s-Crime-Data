import React, { useState } from 'react';
import './style.css';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import FilterOptions from './components/FilterOptions';
import Visualization from './components/Visualization';
import ChartTypeSelector from './components/ChartTypeSelector';
import ChatHistory from './components/ChatHistory';
import Login from './components/Login';
import Signup from './components/Signup';
import './styles/App.css';

function App() {
  const [chartType, setChartType] = useState('pie'); // Default chart type
  const [viewType, setViewType] = useState('chart'); // Default view type
  const [filter, setFilter] = useState('crimeType'); // Default filter
  const [isLoggedIn, setIsLoggedIn] = useState(false) // User logged out by default

  // console.log("Chart type changed to : ", chartType);

  // Handle filter changes
  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  // Handle view type changes (chart or text)
  const handleViewTypeChange = (viewType) => {
    setViewType(viewType); // Correctly update the view type
  };

  const handleLogout = () => {
    // localStorage.removeItem('cc_username');
    setIsLoggedIn(false);
  };

  return (
    <div className="container">
      <Header />
      {!isLoggedIn ? ( // When user is not logged in
        <div className='signup-container'>
          <Signup setIsLoggedIn={setIsLoggedIn} />
          <Login setIsLoggedIn={setIsLoggedIn} />
        </div>
      ) : ( // When user is logged in
        <> 
          <div style={{
            textAlign:"right",
            marginInline:"2rem",
          }}>
            <button style={{
              background: "transparent", 
              fontWeight: "bold", 
              cursor:"pointer",
              color: "#e1e8ed",
              backgroundColor: "#067ec9",
              padding:"10px",
              borderRadius:"10px",
              border:"2px solid #272626" 
              }} onClick={handleLogout}>Log Out</button>
          </div>
          <ChatHistory/>
          <Visualization chartType={chartType} viewType={viewType} />
          
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            }}>
            {viewType === 'chart' && <ChartTypeSelector chartType={chartType} setChartType={setChartType} />}
            {/* <FilterOptions onFilterChange={handleFilterChange} /> */}
          </div>
          <QueryInput setViewType={handleViewTypeChange} />
      </>
      )}
    </div>
  );
}

export default App;
