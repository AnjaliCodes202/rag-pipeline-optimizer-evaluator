#Answer the question:
#“Given the same query and dataset, how do different RAG pipelines perform relative to each other?”
#This is the foundation for evaluation, ranking, and recommendation later.
#Convert raw experiment metrics into a single comparable score:
#Tradeoff Score = Quality / (Cost × Latency)
#This allows the system to answer:
#“Which pipeline gives the best answer for the least money and time?”
# backend/app/core/experiment_runner/comparator.py
#Given already-ranked pipeline results, answer:
#“Which pipeline should be recommended, and why?”
#This is decision explanation, not decision making

from typing import List,Dict,Any
from core.experiment_runner.executor import run_pipeline_experiment

def compare_pipelines(query: str, document_text: str, pipelines: List[Dict[str, Any]], judge_client, reranker=None):
    results = []
    for pipeline in pipelines:
        pipeline_id = pipeline.pipeline_id
        pipeline_config = pipeline.pipeline_config.model_dump()
        experiment_result = run_pipeline_experiment(
            pipeline_id=pipeline_id,
            query=query,
            document_text=document_text,
            pipeline_config=pipeline_config,
            # generator_client=generator_client,
            judge_client=judge_client,
            reranker=reranker
        )
        experiment_result["pipeline_id"] = pipeline_id

        results.append(experiment_result)
    for result in results:
        result['tradeoff_score'] = compute_tradeoff_score(result)
    results.sort(key = lambda x: x['tradeoff_score'],reverse=True)
    return results


def compute_tradeoff_score(experiment_result:Dict[str,Any]):
    evaluation = experiment_result["evaluation"]
    if not evaluation:
        return 0.0
    quality_scores = evaluation.quality_scores

    quality = (
        quality_scores.relevance +
        quality_scores.faithfulness +
        quality_scores.completeness
    )
    cost = experiment_result.get("estimated_cost", 0.0)
    latency = experiment_result.get("total_latency_ms", 0.0)

    if cost<=0 or latency<=0:
        return 0.0
    return quality / (cost * latency)

def recommend_pipeline(ranked_results: List[Dict[str, Any]]):
    if not ranked_results:
        return {
            "recommended_pipeline": None,
            "reason": "No pipeline results available"
        }
    best = ranked_results[0]
    explanation = {
        "pipeline_id": best["pipeline_id"],
        "tradeoff_score": best["tradeoff_score"],
        "quality_breakdown": best["evaluation"].quality_scores,
        "estimated_cost": best["estimated_cost"],
        "total_latency_ms": best["total_latency_ms"],
    }
    reason = (
        "This pipeline provides the best balance of answer quality, "
        "low cost, and low latency based on the tradeoff score."
    )
    return {
        "recommended_pipeline": explanation,
        "reason": reason
    }



