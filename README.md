# AI-Augmented SOC Assistant

An end-to-end **SIEM/SOAR-style cybersecurity platform** that ingests Suricata IDS logs, applies YAML-based detection rules, maps alerts to **MITRE ATT&CK**, and generates **AI-powered incident summaries** using a local Llama 3.2 model (Ollama).

## 🚀 Features
- **Suricata EVE JSON ingestion** via FastAPI (`/ingest`)
- Normalized event storage in SQLite
- **YAML correlation rules** for detection
- Automatic **Incident creation** with severity scoring
- **MITRE ATT&CK technique tagging**
- AI-driven incident summaries (Llama 3.2 via Ollama)
- Modular detection pipeline: parsers → rules → AI → response

## 🛠️ Tech Stack
- Python, FastAPI
- Suricata IDS
- SQLite
- Ollama (local LLM inference)
- YAML rule engine

## 📦 Installation
```bash
pip install -r requirements.txt
uvicorn app.web.api:app --reload
