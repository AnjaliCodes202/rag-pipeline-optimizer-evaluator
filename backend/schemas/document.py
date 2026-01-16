from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

# class DocumentBase(BaseModel):
#     name: str = Field(...,description="Original file name")
#     content_type: Optional[str] = Field(None,description="dataset content type")
#     extracted_text: Optional[str] = Field(None,description="dataset extracted text")
#     dataset_id: Optional[str] = Field(None,description="dataset grouping ID")


# class DocumentInDB(DocumentBase):
#     id:str
#     upload_time:datetime


# class DocumentResponse(DocumentInDB):
#     pass

class DocumentBase(BaseModel):
    name: str = Field(..., description="Original file name")
    dataset_id: Optional[str] = Field(None, description="dataset grouping ID")
    extracted_text: Optional[str] = Field(
        None, description="Extracted document text (for RAG)"
    )


class DocumentInDB(BaseModel):
    id: str
    name: str
    content_type: str
    dataset_id: Optional[str]
    upload_time: datetime
    extracted_text: Optional[str]


class DocumentResponse(DocumentInDB):
    pass
