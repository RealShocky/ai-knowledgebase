from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    DATABASE_URL: str = "sqlite:///./faqrep.db"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
