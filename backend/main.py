from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from utils.logger import setup_logger
from api import documents
from api import experiments

settings = get_settings()
logger = setup_logger()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods = ["*"],    # allows POST, OPTIONS, etc.
    allow_headers = ["*"],    # allows Content-Type, Authorization, etc.
)
app.include_router(documents.router)
app.include_router(experiments.router)

@app.get("/health")
def health_check():
    logger.info("helth check requested")
    return{
        "status":"ok",
        "app":settings.app_name,
        "environment":settings.environment
    }