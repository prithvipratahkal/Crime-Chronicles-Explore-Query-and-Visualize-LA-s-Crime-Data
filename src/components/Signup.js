import React, { useState } from 'react';
import '../styles/Signup.css';


const Signup = ({setIsLoggedIn}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    // const result = signup(username, password);
    
    if(username.length===0 || password.length===0){
        setMessage("Missing Username or Password!");
    }

    if(localStorage.getItem(`cc_${username}`)){
        setMessage("Username already exists!");
    }
    else{
        localStorage.setItem(`cc_${username}`, username);
        localStorage.setItem(`cc_${username}_pw`, password);
        setMessage("User created successfully.!");
        setTimeout(() => {
            setIsLoggedIn(true);
        }, 1000);    
    }
    

    // if (result.success) {
    //   // Store the username in localStorage
    //   localStorage.setItem('cc_username', username);
    // }

    // setMessage(result.message);
  };

  return (
    <div style={{textAlign:"center"}}>
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
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
        <button type="submit">Signup</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Signup;
