import React from "react";
import { useExperimentStore } from "../../store/experimentStore";

export default function CostChart() {
  const results = useExperimentStore((s) => s.comparisonResults);

  if (!results || results.length === 0) {
    return <p>No comparison data available.</p>;
  }

  return (
    <div className="analytics-panel">
      <h3>Cost vs Latency</h3>

      <table>
        <thead>
          <tr>
            <th>Pipeline</th>
            <th>Latency (ms)</th>
            <th>Estimated Cost</th>
            <th>Tradeoff Score</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r) => (
            <tr key={r.pipeline_id}>
              <td>{r.pipeline_id}</td>
              <td>{r.total_latency_ms.toFixed(2)}</td>
              <td>${r.estimated_cost}</td>
              <td>{r.tradeoff_score.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p style={{ marginTop: "8px", fontSize: "0.9em" }}>
        Lower latency and lower cost are better.  
        Higher tradeoff score indicates a more efficient pipeline.
      </p>
    </div>
  );
}
