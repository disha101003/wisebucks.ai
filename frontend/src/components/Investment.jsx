import React from "react";
import "../investment.css";
import Sidebar from "./Sidebar";

const Investment = () => {
  return (
    <div>
      <Sidebar current="investment" />
      <section id="main-dashboard-content">
        <section id="top-section">
          <h1 id="welcome-title">Hello, Sally Norman</h1>
          <div className="action-icons">
            <div className="action-icon-one"></div>
            <span style={{ fontSize: 30, paddingLeft: 10 }}>▾</span>
          </div>
        </section>
        <h2 className="top-dash">INVESTMENT CHALLENGE</h2>
        <section id="grid-container">
          <div className="grid-item one"></div>
          <div className="grid-item two"></div>
        </section>
        <section id="grid-container2">
          <div className="grid-item one"></div>
          <div className="grid-item two"></div>
        </section>
      </section>
    </div>
  );
};

export default Investment;
