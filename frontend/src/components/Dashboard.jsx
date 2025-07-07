import React, { useEffect, useState, useRef } from "react";
import "../dashboard.css";
import Sidebar from "./Sidebar";
import DashboardCard from "./DashboardCard";
import TopInvestedCompanies from "./TopInvestedCompanies";

const TICKERS = [
  "AAPL",
  "ACN",
  "AMZN",
  "GOOGL",
  "META",
  "MSFT",
  "NFLX",
  "NVDA",
  "ORCL",
  "TSLA",
  "V",
  "WMT",
  "XOM",
  "ZM",
];

const StockItem = ({ ticker, data, colorClass, arrowClass, flashClass }) => (
  <div id={ticker} className={`stock-item ${flashClass || ""}`.trim()}>
    <h4 id={`${ticker}-name`} className={`stock-name ${colorClass}`}>
      {ticker}
    </h4>
    <h4 id={`${ticker}-pct`} className={`stock-pct ${colorClass}`}>
      {data ? `${data.changePercent.toFixed(2)}%` : ""}
    </h4>
    <div className="stock-arrow-container">
      <img className={`stock-arrow ${arrowClass || ""}`} alt="arrow" />
    </div>
    <h4 id={`${ticker}-price`} className="stock-stock">
      {data ? data.currentPrice.toFixed(2) : ""}
    </h4>
  </div>
);

const Dashboard = () => {
  const [search, setSearch] = useState("");
  const [stockData, setStockData] = useState({}); // { ticker: { currentPrice, openPrice, changePercent } }
  const [lastPrices, setLastPrices] = useState({});
  const [flash, setFlash] = useState({}); // { ticker: flashClass }
  const [arrow, setArrow] = useState({}); // { ticker: arrowClass }
  const [color, setColor] = useState({}); // { ticker: colorClass }
  const [counter, setCounter] = useState(15);
  const intervalRef = useRef();

  // Filtered tickers based on search
  const filteredTickers = TICKERS.filter((ticker) =>
    ticker.toLowerCase().includes(search.toLowerCase())
  );

  // Fetch stock data for all tickers
  const fetchPrices = async () => {
    const newStockData = { ...stockData };
    const newLastPrices = { ...lastPrices };
    const newFlash = {};
    const newArrow = {};
    const newColor = {};
    await Promise.all(
      filteredTickers.map(async (ticker) => {
        try {
          const res = await fetch("/get_stock_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticker }),
          });
          const data = await res.json();
          const changePercent =
            ((data.currentPrice - data.openPrice) / data.openPrice) * 100;
          let colorClass = "";
          if (changePercent <= -2) colorClass = "dark-red";
          else if (changePercent < 0) colorClass = "red";
          else if (changePercent === 0) colorClass = "gray";
          else if (changePercent <= 2) colorClass = "green";
          else colorClass = "dark-green";

          newStockData[ticker] = { ...data, changePercent };
          newColor[ticker] = colorClass;

          let flashClass = "",
            arrowClass = "";
          if (lastPrices[ticker] > data.currentPrice) {
            flashClass = "red-flash";
            arrowClass = "stock-arrow-red";
          } else if (lastPrices[ticker] < data.currentPrice) {
            flashClass = "green-flash";
            arrowClass = "stock-arrow-green";
          } else {
            flashClass = "gray-flash";
            arrowClass = "stock-arrow-dash";
          }
          newLastPrices[ticker] = data.currentPrice;
          newFlash[ticker] = flashClass;
          newArrow[ticker] = arrowClass;
        } catch (e) {
          // handle error
        }
      })
    );
    setStockData(newStockData);
    setLastPrices(newLastPrices);
    setFlash(newFlash);
    setArrow(newArrow);
    setColor(newColor);
  };

  // Update prices every 15 seconds
  useEffect(() => {
    fetchPrices();
    intervalRef.current = setInterval(() => {
      setCounter((c) => {
        if (c <= 1) {
          fetchPrices();
          return 15;
        }
        return c - 1;
      });
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, [search]);

  useEffect(() => {
    setCounter(15);
  }, [search]);

  const companies = [
    { name: "Apple", amount: "$30,000" },
    { name: "Microsoft", amount: "$25,000" },
    { name: "Tesla", amount: "$20,000" },
  ];

  return (
    <div>
      <Sidebar current="dashboard" />
      <section id="main-dashboard-content">
        <section id="top-section">
          <h1 id="welcome-title">Hello, Sally Norman</h1>
          <div className="action-icons">
            <div className="action-icon-one"></div>
            <span style={{ fontSize: 30, paddingLeft: 10 }}>▾</span>
          </div>
        </section>
        <h2 className="top-dash">DASHBOARD</h2>
        <div className="dash-container">
          <div className="dash-container-left">
            <div className="search-container">
              <img
                src="/images/search.png"
                className="search-icon"
                alt="search"
              />
              <input
                type="text"
                className="search"
                id="chat-input"
                placeholder="Search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div id="stocks" className="stocks-container">
              {filteredTickers.map((ticker) => (
                <StockItem
                  key={ticker}
                  ticker={ticker}
                  data={stockData[ticker]}
                  colorClass={color[ticker]}
                  arrowClass={arrow[ticker]}
                  flashClass={flash[ticker]}
                />
              ))}
            </div>
          </div>
          <div className="dash-container-right">
            <div className="main-container">
              <div className="content-container1">
                <div className="card financial-overview">
                  <DashboardCard title="Available Balance" amount="$50,000" />
                  <DashboardCard
                    title="Daily Returns"
                    percentage="+2.02%"
                    amount="+$2,000"
                  />
                  <DashboardCard
                    title="Total Returns"
                    percentage="+5.75%"
                    amount="+$5,000"
                  />
                </div>
                <div className="card holdings-overview">
                  <div className="holdings-section">
                    <div className="holdings-title">
                      <h2>Holdings (138)</h2>
                    </div>
                    <div className="holdings-chart">
                      <img
                        src="/images/Bar.png"
                        alt="Holdings Chart"
                        style={{ width: "90%", height: "auto" }}
                      />
                    </div>
                  </div>
                  <TopInvestedCompanies companies={companies} />
                </div>
                <div className="card-bottom">
                  <div className="card-bottom-left">
                    <img
                      src="/images/Graph.png"
                      alt="Graph"
                      style={{ width: "100%", height: "auto" }}
                    />
                  </div>
                  <div className="card-bottom-right">
                    <div className="model-controls">
                      <h3>Modify Graph</h3>
                      <form id="model-controls-form">
                        <label htmlFor="stock-select">Select Stock:</label>
                        <select id="stock-select" name="stock">
                          <option value="apple">Apple</option>
                        </select>
                        <label htmlFor="start-date">Start Date:</label>
                        <input type="date" id="start-date" name="start-date" />
                        <label htmlFor="end-date">End Date:</label>
                        <input type="date" id="end-date" name="end-date" />
                        <button type="submit">Update Chart</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
