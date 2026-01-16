// // 1️⃣ PURPOSE (system terms)
// // This component displays answers and metrics returned by the backend.
// // It:
// // reads experiment results from Zustand
// // conditionally renders:
// // single-pipeline result
// // multi-pipeline comparison
// // recommendation result
// // It does not:
// // trigger APIs
// // compute scores
// // decide winners
// import React from "react";
// import { useExperimentStore } from "../../store/experimentStore";

// export default function AnswerComparison() {
//   const runResult = useExperimentStore((s) => s.runResult);
//   const compareResult = useExperimentStore((s) => s.comparisonResults);
//   const recommendResult = useExperimentStore((s) => s.recommendation);

//   if (
//     !runResult &&
//     (!compareResult || compareResult.length === 0) &&
//     !recommendResult
//   ) {
//     return <p>No results yet. Run an experiment to see results.</p>;
//   }

//   if (runResult) {
//     const qs = runResult.evaluation?.quality_scores;
//     return (
//       <div className="result-panel">
//         <h3>Answer</h3>
//         <p>{runResult.answer}</p>

//         <h4>Evaluation Scores</h4>
//         <ul>
//           <li>Relevance: {qs.relevance}</li>
//           <li>Faithfulness: {qs.faithfulness}</li>
//           <li>Completeness: {qs.completeness}</li>
//         </ul>

//         <h4>Cost & Latency</h4>
//         <ul>
//           <li>Estimated Cost: ${runResult.estimated_cost}</li>
//           <li>Total Latency: {runResult.total_latency_ms} milliseconds</li>
//         </ul>
//       </div>
//     );
//   }

//   if (compareResult && compareResult.length > 0) {
//     const bestPipelineId = compareResult[0].pipeline_id;

//     return (
//       <div className="result-panel">
//         <h3>Pipeline Comparison</h3>

//         {compareResult.map((result) => {
//           const qs = result.evaluation?.quality_scores;

//           return (
//             <div
//               key={result.pipeline_id}
//               style={{
//                 border: "1px solid #ccc",
//                 padding: "12px",
//                 marginBottom: "12px",
//                 background:
//                   result.pipeline_id === bestPipelineId ? "#e6fffa" : "white",
//               }}
//             >
//               <h4>
//                 {result.pipeline_id}{" "}
//                 {result.pipeline_id === bestPipelineId && "⭐ BEST"}
//               </h4>

//               <p>
//                 <strong>Tradeoff Score:</strong>{" "}
//                 {result.tradeoff_score.toFixed(4)}
//               </p>

//               {qs && (
//                 <>
//                   <p>
//                     <strong>Quality Breakdown</strong>
//                   </p>
//                   <ul>
//                     <li>Relevance: {qs.relevance}</li>
//                     <li>Faithfulness: {qs.faithfulness}</li>
//                     <li>Completeness: {qs.completeness}</li>
//                   </ul>
//                 </>
//               )}

//               <p>
//                 <strong>Estimated Cost:</strong> ${result.estimated_cost}
//               </p>
//               <p>
//                 <strong>Total Latency:</strong> {result.total_latency_ms} ms
//               </p>
//             </div>
//           );
//         })}
//       </div>
//     );
//   }

//   if (recommendResult) {
//     const rec = recommendResult.recommended_pipeline;
//     const qs = rec.quality_breakdown;
//     return (
//       <div className="result-panel">
//         <h3>Recommended Pipeline</h3>

//         <p>
//           <strong>Pipeline ID:</strong> {rec.pipeline_id}
//         </p>
//         <p>
//           <strong>Tradeoff Score:</strong> {rec.tradeoff_score}
//         </p>

//         <h4>Quality Breakdown</h4>
//         <ul>
//           <li>Relevance: {qs.relevance}</li>
//           <li>Faithfulness: {qs.faithfulness}</li>
//           <li>Completeness: {qs.completeness}</li>
//         </ul>

//         <h4>Cost & Latency</h4>
//         <ul>
//           <li>Estimated Cost: ${rec.estimated_cost}</li>
//           <li>Total Latency: {rec.total_latency_ms} ms</li>
//         </ul>

//         <p>
//           <strong>Reason:</strong> {recommendResult.reason}
//         </p>
//       </div>
//     );
//   }

//   return null;
// }

// AnswerComparison.jsx
import React from "react";
import { useExperimentStore } from "../../store/experimentStore";

export default function AnswerComparison() {
  const runResult = useExperimentStore((s) => s.runResult);
  const comparisonResults = useExperimentStore((s) => s.comparisonResults);
  const recommendation = useExperimentStore((s) => s.recommendation);

  // Nothing to show yet
  if (
    !runResult &&
    (!comparisonResults || comparisonResults.length === 0) &&
    !recommendation
  ) {
    return <p>No results yet. Run an experiment to see results.</p>;
  }

  /* =========================
     SINGLE PIPELINE RESULT
     ========================= */
  if (runResult) {
    const qs = runResult.evaluation?.quality_scores;
    const hall = runResult.evaluation?.hallucination;

    return (
      <div className="result-panel glass-stack">
        {/* ① ANSWER */}
        <section className="answer-section card card-primary">
          <h3>Answer</h3>
          <p>{runResult.answer}</p>
        </section>

        {/* ② QUALITY & RISK */}
        <section className="metrics-section card">
          <h4>Evaluation</h4>
          <div className="metrics-bars">
            <div className="metric">
              <span>Relevance</span>
              <div className="metric-bar">
                <div
                  className="metric-fill"
                  style={{ width: `${qs.relevance * 100}%` }}
                />
              </div>
            </div>

            <div className="metric">
              <span>Faithfulness</span>
              <div className="metric-bar">
                <div
                  className="metric-fill"
                  style={{ width: `${qs.faithfulness * 100}%` }}
                />
              </div>
            </div>

            <div className="metric">
              <span>Completeness</span>
              <div className="metric-bar">
                <div
                  className="metric-fill"
                  style={{ width: `${qs.completeness * 100}%` }}
                />
              </div>
            </div>
          </div>

          <h4>Hallucination</h4>
          <div
            className={`hallucination-banner ${
              hall?.hallucinated ? "danger" : "safe"
            }`}
          >
            <span>
              {hall?.hallucinated
                ? "❌ Hallucination Detected"
                : "✅ No Hallucination"}
            </span>
            <span>Confidence: {hall?.confidence}</span>
          </div>
        </section>

        {/* ③ COST & LATENCY */}
        <section className="cost-section card card-muted">
          <h4>Cost & Latency</h4>
          <ul>
            <li>Estimated Cost: ${runResult.estimated_cost}</li>
            <li>Total Latency: {runResult.total_latency_ms} ms</li>
          </ul>
        </section>
      </div>
    );
  }

  /* =========================
     PIPELINE COMPARISON
     ========================= */
  if (comparisonResults && comparisonResults.length > 0) {
    return (
      <div className="result-panel">
        <h3>Pipeline Comparison</h3>
        <table>
          <thead>
            <tr>
              <th>Pipeline</th>
              <th>Quality</th>
              <th>Cost</th>
              <th>Latency (ms)</th>
              <th>Tradeoff Score</th>
            </tr>
          </thead>
          <tbody>
            {comparisonResults.map((res, index) => {
              const qs = res.evaluation?.quality_scores;
              const quality = qs.relevance + qs.faithfulness + qs.completeness;

              const isBest = index === 0;

              return (
                <tr key={res.pipeline_id} className={isBest ? "best-row" : ""}>
                  <td>{res.pipeline_id}</td>
                  <td>{quality.toFixed(3)}</td>
                  <td>${res.estimated_cost}</td>
                  <td>{res.total_latency_ms}</td>
                  <td className="tradeoff-score">
                    {res.tradeoff_score.toFixed(4)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }

  /* =========================
     RECOMMENDATION
     ========================= */
  if (recommendation) {
    const rec = recommendation.recommended_pipeline;
    return (
      <div className="result-panel">
        <h3>Recommended Pipeline</h3>
        <p>
          <strong>Pipeline ID:</strong> {rec.pipeline_id}
        </p>
        <p>
          <strong>Tradeoff Score:</strong> {rec.tradeoff_score}
        </p>
        <p>{recommendation.reason}</p>
      </div>
    );
  }

  return null;
}
