# app/ai/ollama_client.py
import httpx
from ..config import settings

def generate_ollama(prompt: str) -> str:
    """
    Call the local Ollama server and return the generated text.
    Synchronous call for simplicity.
    """
    url = settings.ollama_endpoint.rstrip("/") + "/api/generate"
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    resp = httpx.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    # Ollama returns {"response": "...", "done": true, ...}
    text = data.get("response", "").strip()
    return text

