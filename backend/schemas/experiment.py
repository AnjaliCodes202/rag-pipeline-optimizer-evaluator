from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.pipeline import PipelineBase
from schemas.evaluation import EvaluationResult



class RunExperimentRequest(BaseModel):
    pipeline_id: Optional[str] = Field(None, description="Existing pipeline ID to use")
    query: str = Field(..., description="User question")
    document_text: str = Field(..., description="Extracted document text")
    pipeline_config: PipelineBase

class PipelineWithId(BaseModel):
    pipeline_id: str
    pipeline_config: PipelineBase

class ComparePipelinesRequest(BaseModel):
    query: str = Field(..., description="User question")
    document_text: str = Field(..., description="Extracted document text")
    pipelines: List[PipelineWithId]


class RetrievedChunk(BaseModel):
    text: str
    similarity_score: float


class RunExperimentResult(BaseModel):
    answer: str
    retrieved_chunks: List[RetrievedChunk]
    evaluation: Optional[EvaluationResult]
    embedding_time_ms: float = 0.0
    retrieval_time_ms: float = 0.0
    generation_time_ms: float = 0.0
    total_latency_ms: float = 0.0

    estimated_cost: float = 0.0
    



class PipelineRunResult(BaseModel):
    pipeline_id: Optional[str] = Field(None, description="Existing pipeline ID to use")
    pipeline_config: PipelineBase
    result: RunExperimentResult


class ComparePipelinesResult(BaseModel):
    results: List[PipelineRunResult]


class PipelineWithId(BaseModel):
    pipeline_id: str
    pipeline_config: PipelineBase