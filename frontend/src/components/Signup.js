import React, { useState } from 'react';
import '../styles/Signup.css';


const Signup = ({setIsLoggedIn, setUsername, setPassword, username, password}) => { 
  const [signupMessage, setSignupMessage] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    // const result = signup(username, password);
    
    if(username.length===0 || password.length===0){
        setSignupMessage("Missing Username or Password!");
    }

    if(localStorage.getItem(`cc_${username}`)){
        setSignupMessage("Username already exists!");
    }
    else{
        localStorage.setItem(`cc_${username}`, username);
        localStorage.setItem(`cc_${username}_pw`, password);
        setSignupMessage("User created successfully.!");
        setTimeout(() => {
            setIsLoggedIn(true);
        }, 1500);    
    }
    

    // if (result.success) {
    //   // Store the username in localStorage
    //   localStorage.setItem('cc_username', username);
    // }

    // setMessage(result.message);
  };

  return (
    <div className='signup-div'>
      <div>
        <small>New User?</small>
        <h2>Sign Up</h2>
      </div>
      <form onSubmit={handleSignup}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Signup</button>
      </form>
      {signupMessage && <p>{signupMessage}</p>}
    </div>
  );
};

export default Signup;
