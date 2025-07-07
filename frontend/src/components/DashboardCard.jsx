import React from "react";

const DashboardCard = ({ title, percentage, amount }) => (
  <div className="card-section">
    <h2>{title}</h2>
    {percentage && <p className="percentage-right">{percentage}</p>}
    <p className="amount">{amount}</p>
  </div>
);

export default DashboardCard;
