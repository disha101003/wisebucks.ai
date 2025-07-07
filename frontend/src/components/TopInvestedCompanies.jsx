import React from "react";

const TopInvestedCompanies = ({ companies }) => (
  <div className="top-invested-companies">
    <h3>Top Investments</h3>
    {companies.map((company, idx) => (
      <div className="company-row" key={idx}>
        <span>{company.name}</span>
        <span>{company.amount}</span>
      </div>
    ))}
  </div>
);

export default TopInvestedCompanies;
