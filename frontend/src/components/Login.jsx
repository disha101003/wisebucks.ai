import React from "react";
import "../login.css";

const Login = () => {
  return (
    <div className="login-container">
      <h2>Login</h2>
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button className="login-button" type="submit">
          Login
        </button>
      </form>
      <h5>
        Don't have an account? <a href="/signup">Sign up</a>
      </h5>
    </div>
  );
};

export default Login;
