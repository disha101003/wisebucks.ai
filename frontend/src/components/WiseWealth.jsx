import React from "react";
import "../wisewealth.css";
import Sidebar from "./Sidebar";

const WiseWealth = () => {
  return (
    <div>
      <Sidebar current="wisewealth" />
      <section id="main-dashboard-content">
        <section id="top-section">
          <h1 id="welcome-title">Hello, Sally Norman</h1>
          <div className="action-icons">
            <div className="action-icon-one"></div>
            <span style={{ fontSize: 30, paddingLeft: 10 }}>▾</span>
          </div>
        </section>
        <h2 className="top-dash">WISEWEALTH</h2>
        <section id="grid-container">
          <div className="grid-item one">
            <img
              src="/images/graph.png"
              style={{ width: 500, height: 300 }}
              alt="graph"
            />
          </div>
          <div className="grid-item two">
            <h5
              style={{ backgroundColor: "rgb(93, 232, 58)", fontWeight: 500 }}
            >
              Positive Sentiment (9.8/10)
            </h5>
            <h5>
              "NVIDIA (NASDAQ: NVDA) reported a record revenue of $18.12 billion
              for the third quarter, up 206% from a year ago and up 34% from the
              previous quarter."
            </h5>
            <br />
            <br />
            <h5
              style={{ backgroundColor: "rgb(200, 81, 81)", fontWeight: 500 }}
            >
              Negative Sentiment (2.2/10)
            </h5>
            <h5>
              "US FDA flags a new problem with Philips machines, causing shares
              to fall".
            </h5>
            <br />
            <br />
            <h5
              style={{ backgroundColor: "rgb(136, 210, 136)", fontWeight: 500 }}
            >
              Positive Sentiment (7.5/10)
            </h5>
            <h5>
              "GM surges after stock buyback, dividend announcement": Wall
              Street's top analyst calls".
            </h5>
          </div>
        </section>
        <section id="grid-container2">
          <div className="grid-item one">
            <h2>Why buy AAPL for the next 3 months:</h2>
            <br />
            <h1>
              Given your current portfolio, investing in Apple Inc. (AAPL) in
              the upcoming quarter is promising, driven by positive news
              sentiment from its innovative product launches, strong
              fundamentals with a recent reported revenue of over $83 billion,
              and a historical pattern of stock resilience. AAPL has
              consistently shown robust growth, with its stock price often
              outperforming market expectations and swiftly recovering from
              downturns, indicating a solid investment choice.
            </h1>
          </div>
          <div className="grid-item two">
            <h2>Stock Predictions:</h2>
            <br />
            <h1>
              AAPL: 📈 Sentiment 8.8/10; Q3 Rev &gt;$83B; 📊 historical trend ↑;
              🟢 Buy Signal
            </h1>
            <br />
            <h1>
              TSLA: 📉 Sentiment 2.2/10; 💰 Q3 Rev $23.35B (↓ from Q2); 📊 Stock
              -20% since July; 🔴 Sell Signal.
            </h1>
          </div>
        </section>
      </section>
    </div>
  );
};

export default WiseWealth;
