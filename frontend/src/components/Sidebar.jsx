import React from "react";

const Sidebar = ({ current }) => (
  <section id="sidebar">
    <a href="/" style={{ textDecoration: "none", color: "#003260" }}>
      <section className="title-container">
        <img src="/images/logo.png" width="40px" alt="logo" />
        <h1>WISEBUCK.AI</h1>
      </section>
    </a>
    <section className="links-container">
      <h2>FEATURES</h2>
      <div
        className={`links${current === "dashboard" ? " active" : ""}`}
        style={{ color: current === "dashboard" ? "#e8349c" : undefined }}
      >
        <div className="icon">
          <i
            className="fa-solid fa-object-group"
            style={{ color: current === "dashboard" ? "#e8349c" : undefined }}
          ></i>
        </div>
        <span>Dashboard</span>
      </div>
      <div className="vl"></div>
      <div className={`links${current === "investment" ? " active" : ""}`}>
        <div className="icon">
          <i className="fas fa-chart-bar"></i>
        </div>
        <a href="/investment">
          <span>Investment Challenge</span>
        </a>
      </div>
      <div className={`links${current === "trading" ? " active" : ""}`}>
        <div className="icon">
          <i className="fa-solid fa-file-lines"></i>
        </div>
        <a href="/trading">
          <span>Paper Trading</span>
        </a>
      </div>
      <div className={`links${current === "wisewealth" ? " active" : ""}`}>
        <div className="icon">
          <i className="fa-solid fa-sack-dollar"></i>
        </div>
        <a href="/wisewealth">
          <span>WiseWealth</span>
        </a>
      </div>
      <h2>DOCUMENTATION</h2>
      <div className="links" style={{ marginTop: "-7px" }}>
        <div className="icon">
          <i className="fa-brands fa-youtube"></i>
        </div>
        <button
          style={{
            background: "none",
            border: "none",
            color: "#003260",
            cursor: "pointer",
            padding: 0,
          }}
          onClick={() => alert("Tutorials coming soon!")}
        >
          <span>Tutorials</span>
        </button>
      </div>
      <div className="chatbot-button-container">
        <a className="chatbot-button" href="/chatbot">
          <i className="fa-solid fa-robot" style={{ paddingRight: 10 }}></i>
          LAUNCH CHATBOT
        </a>
      </div>
    </section>
  </section>
);

export default Sidebar;
