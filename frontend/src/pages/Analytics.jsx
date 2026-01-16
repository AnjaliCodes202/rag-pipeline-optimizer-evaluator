import React from "react";
import CostChart from "../components/analytics/CostChart";

export default function Analytics() {
  return (
    <div className="page analytics-page">
      <h2>Analytics</h2>
      <p>
        Visual analysis of RAG pipeline performance across cost, latency, and
        quality.
      </p>

      <CostChart />
    </div>
  );
}
