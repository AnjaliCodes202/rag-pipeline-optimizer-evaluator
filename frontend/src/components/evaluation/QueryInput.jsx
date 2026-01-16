// 1️⃣ PURPOSE (system terms)
// This component captures the user’s question and stores it in global state.
// It:
// updates query in Zustand
// does not call APIs
// does not trigger execution
// Execution is handled only by the Action Panel (correct separation).

import React from "react";
import { useExperimentStore } from "../../store/experimentStore";

export default function QueryInput(){
  const query = useExperimentStore((state) => state.query);
  const setQuery = useExperimentStore((state) => state.setQuery);
  const handleChange = (e) => {
    setQuery(e.target.value);
    //                It gives the current value entered by the user in an input field.
  };
  return (
      <div className="query-panel">
            <label htmlFor="query-input">
                  Ask a question:
            </label>
            <textarea id="query-input" value={query} onChange={handleChange} placeholder="e.g. what is the company policy on remote work?" rows={3}/>
      </div>
  );
};
