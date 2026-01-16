#Turn raw execution into a measured experiment result.
#This answers the question:
#“What did this pipeline answer, and how good was that answer?”

# PURPOSE (system terms)
# Collect all outputs of one experiment run into a single structured object.
# This file does not execute logic — it organizes results.

from typing import Dict,Any
def track_experiment_run(pipeline_id:str, query:str, execution_result:Dict[str,Any], evaluation_scores: Dict[str,float]):
    return {
        "pipeline_id": pipeline_id,
        "query": query,
        "answer": execution_result["answer"],
        "retrieved_chunks": execution_result["retrieved_chunks"],
        "evaluation": evaluation_scores
    }