from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from pathlib import Path
import shutil
from core.ingestion.ingest_document import ingest_document
from schemas.document import DocumentBase,DocumentResponse
from services.document_service import DocumentService

document_service = DocumentService()
router = APIRouter(prefix="/documents",tags=["Documents"])


@router.post("/",response_model=DocumentResponse)
async def create_Documents(document: DocumentBase):
    try:
        response = await document_service.create_document(
            name=document.name,
            content_type=document.content_type,
            extracted_text=document.extracted_text,
            dataset_id=document.dataset_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))



@router.get("/", response_model=List[DocumentResponse])
async def list_documents():
    documents = []

    cursor = document_service.collection.find()
    async for doc in cursor:
        documents.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "dataset_id": doc.get("dataset_id"),
            "content_type": doc["content_type"],
            "extracted_text": doc.get("extracted_text"),
            "upload_time": doc["upload_time"]
        })

    return documents

@router.post("/upload",response_model=DocumentResponse)
async def upload_document(file:UploadFile = File(...), dataset_id:str|None=None):
    file_ext = file.filename.split(".")[-1].lower()
    save_path = Path("uploaded_files")/file.filename
    save_path.parent.mkdir(exist_ok=True)
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = ingest_document(save_path, file_ext)
        created = await document_service.create_document(
            name=file.filename,
            content_type=file_ext,
            extracted_text=extracted_text,
            dataset_id=dataset_id
            
        )
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

