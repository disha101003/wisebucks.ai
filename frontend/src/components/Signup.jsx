import React from "react";
import "../login.css";

const Signup = () => {
  return (
    <div className="login-container">
      <h2>Sign Up</h2>
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <input type="email" placeholder="Email" />
        <button className="login-button" type="submit">
          Sign Up
        </button>
      </form>
      <h5>
        Already have an account? <a href="/login">Login</a>
      </h5>
    </div>
  );
};

export default Signup;
