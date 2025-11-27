# app/ai/summarizer.py
from textwrap import shorten
from ..models import Incident, Event
from .ollama_client import generate_ollama

PROMPT_TEMPLATE = """
You are a senior SOC analyst.

Summarize the following security incident in 4–6 bullet points.

Rules:
- If you are NOT sure of the exact MITRE ATT&CK technique ID, say "MITRE ATT&CK: Unknown" instead of inventing one.
- Use ONLY real techniques like "T1071.001 Web Protocols" IF you are confident. Otherwise say "Unknown".
- Focus on: what probably happened, impact, and concrete remediation steps.
- Keep the language clear and professional.
- Maximum 180 words.

Incident data (JSON-like):
{incident_data}

Event data (JSON-like):
{event_data}
"""


def summarize_incident(incident: Incident, event: Event) -> str:
    incident_data = incident.data or {}
    event_data = event.raw or {}

    prompt = PROMPT_TEMPLATE.format(
        incident_data=incident_data,
        event_data=event_data,
    )

    try:
        text = generate_ollama(prompt)
        # keep summary reasonably short for DB
        return shorten(text, width=800, placeholder="...")
    except Exception as e:
        print(f"[ai] Error generating summary: {e}")
        return "Summary unavailable (AI error)."
