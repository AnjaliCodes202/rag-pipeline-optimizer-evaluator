from pydantic import BaseModel, Field
from typing import Literal

class PipelineBase(BaseModel):
    chunking_strategy: str = "fixed"
    chunk_size: int = Field(..., gt=0)
    chunk_overlap: int = Field(..., ge=0)
    top_k: int = Field(..., gt=0)

    embedding_model: Literal[
        "minilm",
        "mpnet",
        "bge"
    ]

    generator_model: Literal[
          "distilgpt2",
          "facebook/opt-125m",
          "facebook/opt-350m",
          "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    ]

    
    temperature: float = Field(0.2, ge=0.0, le=1.0)
    reranker: bool = False

class PipelineResponse(PipelineBase):
    id: str
