from fastapi import APIRouter, HTTPException
from typing import List,Dict,Any

from schemas.experiment import (RunExperimentRequest, RunExperimentResult, ComparePipelinesRequest)

from core.experiment_runner.executor import run_pipeline_experiment
from core.experiment_runner.comparator import (compare_pipelines, recommend_pipeline)

# from core.embeddings import generate_embeddings, DummyEmbeddingClient
from core.generation import HFGeneratorClient
from core.judge import OpenAIJudgeClient
from core.reranking import DummyCrossEncoderReranker

from config import get_settings, Settings   


router = APIRouter(prefix="/experiments", tags=["Experiments"])
settings = get_settings()
# embedding_client = DummyEmbeddingClient()
# def __init__(
#         self,
#         model: str,
#         temperature: float = 0.2,
#         max_new_tokens: int = 250,
#     ):
# generator_client = OpenAIGeneratorClient(model=settings.generator_model,temperature=settings.generator_temperature,max_new_tokens=settings.generator_max_new_tokens)
judge_client = OpenAIJudgeClient()
reranker = DummyCrossEncoderReranker()


# Expected payload(JSON)
# {
#   "pipeline_id": "pipeline_A",
#   "query": "What is the policy?",
#   "document_text": "...",
#   "pipeline_config": { ... }
# }
@router.post("/run", response_model=RunExperimentResult)
async def run_single_pipeline_experiment(payload:RunExperimentRequest):
    try:
        result = run_pipeline_experiment(
            pipeline_id=payload.pipeline_id,
            query=payload.query,
            document_text=payload.document_text,
            pipeline_config=payload.pipeline_config.model_dump(),
            # generator_client=generator_client,
            judge_client=judge_client,
            reranker=reranker
        )
        return result
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


#expected payload
# {
#   "query": "...",
#   "document_text": "...",
#   "pipelines": [
#     {
#       "pipeline_id": "A",
#       "pipeline_config": { ... }
#     },
#     {
#       "pipeline_id": "B",
#       "pipeline_config": { ... }
#     }
#   ]
# }
@router.post("/compare")
async def compare_multiple_pipeline(payload:ComparePipelinesRequest):
    try:
        results = compare_pipelines(
            query=payload.query,
            document_text=payload.document_text,
            pipelines=payload.pipelines,
            # embedding_client=embedding_client,
            # generator_client=generator_client,
            judge_client=judge_client,
            reranker=reranker
        )
        return results
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required feild: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Expected payload
# {
#   "query": "...",
#   "document_text": "...",
#   "pipelines": [ ... ]
# }
@router.post("/recommend")
async def recommend_best_pipeline(payload:ComparePipelinesRequest):
    try:
        ranked_results = compare_pipelines(
               query=payload.query,
               document_text=payload.document_text,
               pipelines=payload.pipelines,
               judge_client=judge_client,
               reranker=reranker
            ) 

        recommendation = recommend_pipeline(ranked_results)
        return recommendation
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required feild: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




