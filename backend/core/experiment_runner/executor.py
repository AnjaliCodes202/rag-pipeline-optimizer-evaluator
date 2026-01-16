# # backend/app/core/experiment_runner/executor.py
# Provide a single function that answers the question:
# “Given a query + documents + pipeline config, what answer does this pipeline produce?”
# This is the execution core of the RAG system.

from typing import Dict,Any

from core.chunking import chunk_text_with_pipeline
from core.embeddings import generate_embeddings, get_embedding_client
from core.retrieval import retrieve_top_k
from core.reranking import rerank_chunks
from core.generation import generate_answer, get_generator_client
from core.judge import evaluate_answer
from core.experiment_runner.tracker import track_experiment_run
from utils.observability.metrics import track_latency
from services.cost_tracker import calculate_cost
from schemas.experiment import RetrievedChunk


def execute_single_pipeline(query:str, document_text:str, pipeline_config:Dict[str,Any], reranker=None):
    """
    Runs pure RAG execution for a single pipeline.
    No evaluation, no tracking, no persistence.
    """
     
    timings: Dict[str, float] = {}

    # chunking
    chunks = chunk_text_with_pipeline(document_text,pipeline_config)
    # Embeddings
    
    embedding_client = get_embedding_client( pipeline_config["embedding_model"])
    with track_latency(timings, "embedding_time_ms"):
        chunk_embeddings = generate_embeddings(chunks,embedding_client)
        query_embedding = generate_embeddings([query],embedding_client)[0]
    # Retrieval
    with track_latency(timings, "retrieval_time_ms"):
        retrieved = retrieve_top_k(query_embedding=query_embedding, chunk_embeddings=chunk_embeddings, chunks=chunks, top_k=pipeline_config["top_k"])
    # optional reranking
    if pipeline_config.get("reranker") and reranker:
        retrieved = rerank_chunks(
            query=query,
            retrieved_chunks=retrieved,
            reranker=reranker
        )
    selected_chunks = [chunk for chunk,_ in retrieved]
    # Generation
    generator_client = get_generator_client(
          generator_model=pipeline_config["generator_model"],
          temperature=pipeline_config["temperature"]
   )


    with track_latency(timings, "generation_time_ms"):
         answer = generate_answer(query=query,chunks = selected_chunks,generator=generator_client)

    return {
        "answer":answer,
        "retrieved_chunks":retrieved,
        "timings": timings  
    }

def run_pipeline_experiment(pipeline_id: str, query: str, document_text: str, pipeline_config: Dict[str, Any], judge_client, reranker=None):
    """
    Full experiment run:
    RAG execution + evaluation + cost + latency
    """
    total_timings: Dict[str, float] = {}
    metrics: Dict[str, float] = {}
    with track_latency(metrics, "total_latency_ms"):
        execution_result = execute_single_pipeline(
            query=query,
            document_text=document_text,
            pipeline_config=pipeline_config,
            reranker=reranker
        )
    retrieved_chunks = [RetrievedChunk(text=text, similarity_score=score) for text, score in execution_result["retrieved_chunks"]]

    retrieved_texts = [c.text for c in retrieved_chunks]
    # cost tracking
    cost_metrics = calculate_cost(embedding_text=retrieved_texts, generated_text=execution_result['answer'])

    # evaluation
    evaluation_scores = None
    if judge_client:
      evaluation_scores = evaluate_answer(
        question=query,
        answer=execution_result["answer"],
        retrieved_chunks=retrieved_texts,
        judge_client=judge_client
      )
    # experiment_result = track_experiment_run(
    #     pipeline_id=pipeline_id,
    #     query=query,
    #     execution_result=execution_result,
    #     evaluation_scores=evaluation_scores
    # )
    # experiment_result["latency"] = metrics
    # experiment_result["cost"] = cost_metrics
    return {
        # "pipeline_id": pipeline_id,
        "answer": execution_result["answer"],
        "retrieved_chunks": retrieved_chunks,
        "evaluation": evaluation_scores,
         # timing (schema fields)
        "embedding_time_ms": execution_result["timings"].get("embedding_time_ms", 0.0),
        "retrieval_time_ms": execution_result["timings"].get("retrieval_time_ms", 0.0),
        "generation_time_ms": execution_result["timings"].get("generation_time_ms", 0.0),
        "total_latency_ms": metrics.get("total_latency_ms", 0.0),
        # cost
        "estimated_cost": cost_metrics["total_cost"],
    }





