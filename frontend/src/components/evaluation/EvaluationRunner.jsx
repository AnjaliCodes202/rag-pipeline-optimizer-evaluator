// 1️⃣ PURPOSE (system terms)
// This component is the execution controller of the dashboard.
// It:
// triggers backend APIs via Zustand actions
// controls loading & error display
// decides which action to run (Run / Compare / Recommend)
// It does not:
// store input data
// render results
// compute anything
// User clicks button
//  → EvaluationRunner.jsx (THIS FILE)
//    → Zustand action
//      → API call
//        → Backend
//          → Response
//    → Store updates
//  → Results Panel renders
import React from "react";
import { useExperimentStore } from "../../store/experimentStore";

export default function EvaluationRunner() {
  const store = useExperimentStore();
  console.log("STORE SNAPSHOT:", store);
  const loading = useExperimentStore((state) => state.loading);
  const error = useExperimentStore((state) => state.error);
  const pipelines = useExperimentStore((state) => state.pipelines);
  const runSinglePipeline = useExperimentStore(
    (state) => state.runSinglePipeline
  );
  const compareAllPipelines = useExperimentStore(
    (state) => state.compareAllPipelines
  );
  const recommendBestPipeline = useExperimentStore(
    (state) => state.recommendBestPipeline
  );
  const hasPipelines = pipelines.length > 0;
  const handleRun = () => {
    console.log("Run button clicked");
    if (!hasPipelines) {
      console.log("No pipelines found");
      return;
    }
    runSinglePipeline(pipelines[0]);
  };
  const handleCompare = () => {
    if (!hasPipelines) return;
    compareAllPipelines();
  };
  const handleRecommend = () => {
    if (!hasPipelines) return;
    recommendBestPipeline();
  };
  return (
    <div className="action-panel">
      <div className="action-buttons">
        <button
          className="btn-primary"
          onClick={handleRun}
          disabled={loading || !hasPipelines}
        >
          Run Single Pipeline
        </button>

        <button
          className="btn-secondary"
          onClick={handleCompare}
          disabled={loading || !hasPipelines}
        >
          Compare All Pipelines
        </button>

        <button
          className="btn-secondary"
          onClick={handleRecommend}
          disabled={loading || !hasPipelines}
        >
          Recommend Best Pipeline
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}
