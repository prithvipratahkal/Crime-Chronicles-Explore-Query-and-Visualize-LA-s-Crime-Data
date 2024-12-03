import React, { useState } from 'react';
import '../styles/Signup.css';


const Login = ({setIsLoggedIn}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // const result = login(username, password);

    if(localStorage.getItem(`cc_${username}_pw`) === password){
        setIsLoggedIn(true);
    }
    else{
        setMessage("Username or Password is incorrect!");
    }

    // if (result.success) {
    //   // Store the username in localStorage
    //   localStorage.setItem('cc_username', username);
    // }

    // setMessage(result.message);
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Login;
