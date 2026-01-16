from pydantic import BaseModel, Field
from typing import Optional


class QualityScores(BaseModel):
    relevance: float = Field(..., ge=0.0, le=1.0)
    faithfulness: float = Field(..., ge=0.0, le=1.0)
    completeness: float = Field(..., ge=0.0, le=1.0)


class HallucinationAnalysis(BaseModel):
    hallucinated: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    cause: Optional[str] = None


class RetrievalCoverage(BaseModel):
    coverage_score: float = Field(..., ge=0.0, le=1.0)
    missing_sections: Optional[str] = None


class EvaluationResult(BaseModel):
    quality_scores: QualityScores
    hallucination: HallucinationAnalysis
    retrieval_coverage: RetrievalCoverage
    judge_reasoning: Optional[str] = None
