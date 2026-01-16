from datetime import datetime
from db.models import DOCUMENT_COLLECTION
from db.database import get_database

class DocumentService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[DOCUMENT_COLLECTION]

    async def create_document(self, name:str, content_type:str, dataset_id:str | None = None, extracted_text:str | None = None):
        document = {
            "name": name,
            "content_type": content_type,
            "extracted_text": extracted_text,
            "dataset_id": dataset_id,
            "upload_time": datetime.utcnow()
        }
        result = await self.collection.insert_one(document)
        document['id'] = str(result.inserted_id)
        return document

