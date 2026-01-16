//1️⃣ PURPOSE (system terms)
//This file is a pure HTTP adapter.
//It:
//sends requests to backend experiment APIs
//returns parsed JSON responses
//It does not:
//store state
//transform data
//make decisions
//handle UI logic
//Think of it as a wire between frontend state and backend intelligence.

import apiClient from "./apiclient"


export async function runExperiment(payload){
      const response = await apiClient.post("/experiments/run", payload);
      return response.data;
}

export async function comparePipelines(payload){
     const response = await apiClient.post("/experiments/compare",payload);
     return response.data;
}
export async function recommendPipeline(payload){
     const response = await apiClient.post("/experiments/recommend", payload)
     return response.data
}