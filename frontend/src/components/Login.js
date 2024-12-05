import React, { useState } from 'react';
import '../styles/Signup.css';


const Login = ({setIsLoggedIn, setUsername, setPassword, username, password}) => {
  const [loginMessage, setLoginMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // const result = login(username, password);

    if(localStorage.getItem(`cc_${username}_pw`) === password){
        setIsLoggedIn(true);
    }
    else{
        setLoginMessage("Username or Password is incorrect!");
    }

    // if (result.success) {
    //   // Store the username in localStorage
    //   localStorage.setItem('cc_username', username);
    // }

    // setMessage(result.message);
  };

  return (
    <div className='login-div'>
      <div>
        <small>Already a User?</small>
        <h2>Log In</h2>
      </div>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            onChange={(e) => setUsername(e.target.value)}
            required
            data-testid="username"
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            onChange={(e) => setPassword(e.target.value)}
            required
            data-testid="password"
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {loginMessage && <p>{loginMessage}</p>}
    </div>
  );
};

export default Login;
