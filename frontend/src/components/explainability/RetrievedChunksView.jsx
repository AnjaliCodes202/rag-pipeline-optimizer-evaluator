// 1️⃣ PURPOSE (system terms)
// This component explains why the model answered the way it did.
// It:
// displays retrieved chunks used during generation
// shows similarity scores (if provided)
// helps debug retrieval quality
// It does not:
// rerank chunks
// recompute similarity
// judge correctness
// This is pure transparency, not logic.

import React from "react";
import { useExperimentStore } from "../../store/experimentStore";
// [
//   [chunkText, similarityScore],
//   ...
// ]

export default function RetrievedChunkView() {
  const runResult = useExperimentStore((state) => state.runResult);

  if (!runResult || !runResult.retrieved_chunks) {
    return <p>No retrieved chunks to display.</p>;
  }

  if (runResult.retrieved_chunks.length === 0) {
    return <p>No chunks were retrieved for this query.</p>;
  }

  return (
    <div className="retrieved-chunks-panel">
      <h4>Retrieved Chunks</h4>

      {runResult.retrieved_chunks.map((chunk, index) => {
        const score = chunk.similarity_score ?? 0;

        return (
          <div key={index} className="retrieved-chunk-card">
            <div className="chunk-header">
              <span className="chunk-index">Chunk {index + 1}</span>
              <span className="chunk-score">{score.toFixed(3)}</span>
            </div>

            <div className="similarity-bar">
              <div
                className="similarity-fill"
                style={{ width: `${Math.min(score * 100, 100)}%` }}
              />
            </div>

            <p className="chunk-text">{chunk.text}</p>
          </div>
        );
      })}
    </div>
  );
}
