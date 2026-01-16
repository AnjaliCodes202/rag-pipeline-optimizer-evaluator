from pydantic_settings import BaseSettings
from pydantic import Field

from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "rag-optimizer-and-evaluation"
    environment: str = Field(default="development")
    mongodb_uri: str = Field(default="mongodb://localhost:27017")
    mongodb_db_name: str = Field(default="rag_optimizer")
    log_level: str = Field(default="INFO")
    generator_model: str = Field(default="gpt-4o-mini")
    generator_temperature: float = Field(default=0.2)   
    generator_max_new_tokens: int = Field(default=250)
    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()

