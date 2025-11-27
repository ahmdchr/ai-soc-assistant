# app/config.py
import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Adaptive SOC Assistant"
    db_url: str = os.getenv("DB_URL", "sqlite:///./soc.db")

    # 🔥 Ollama config
    ollama_endpoint: str = os.getenv("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

settings = Settings()
