import React from "react";
import "../trading.css";
import Sidebar from "./Sidebar";

const Trading = () => {
  return (
    <div>
      <Sidebar current="trading" />
      <section id="main-dashboard-content">
        <section id="top-section">
          <h1 id="welcome-title">Hello, Sally Norman</h1>
          <div className="action-icons">
            <div className="action-icon-one"></div>
            <span style={{ fontSize: 30, paddingLeft: 10 }}>▾</span>
          </div>
        </section>
        <h2 className="top-dash">PAPER TRADING</h2>
        <section id="grid-container">
          <div className="grid-item one">
            <h3>Simulate Trades</h3>
            <p>Practice trading stocks in a risk-free environment.</p>
          </div>
          <div className="grid-item two">
            <h3>Leaderboard</h3>
            <p>See how you rank against other users in paper trading.</p>
          </div>
        </section>
        <section id="grid-container2">
          <div className="grid-item one">
            <h3>Portfolio Overview</h3>
            <p>Track your simulated holdings and performance.</p>
          </div>
          <div className="grid-item two">
            <h3>Recent Trades</h3>
            <p>Review your latest simulated buy/sell actions.</p>
          </div>
        </section>
      </section>
    </div>
  );
};

export default Trading;
