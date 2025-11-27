# app/detect/rules.py
import yaml
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from ..ai.summarizer import summarize_incident

from ..models import Event, Incident
from .correlate import rule_matches

RULES_DIR = Path("rules")

def load_rules() -> List[Dict[str, Any]]:
    rules: List[Dict[str, Any]] = []
    if not RULES_DIR.exists():
        return rules

    for path in RULES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(path.read_text())
            if isinstance(data, dict):
                rules.append(data)
        except Exception as e:
            print(f"[rules] Error loading {path}: {e}")
    return rules

RULES = load_rules()


def run_detection_pipeline(db: Session, event: Event) -> None:
    """
    Run all rules against a single event.
    For each match, create an Incident.
    """
    if not RULES:
        return

    for rule in RULES:
        if rule_matches(rule, event):
            # Build incident
            title = f"Rule match: {rule.get('id', 'unknown')}"
            severity = rule.get("default_severity", "medium")
            technique = rule.get("technique", "")

            incident = Incident(
                title=title,
                severity=severity,
                technique=technique,
                data={
                    "event_id": event.id,
                    "rule_id": rule.get("id"),
                    "rule_description": rule.get("description"),
                },
            )
            db.add(incident)
            db.commit()
            db.refresh(incident)

            # 🔥 AI summary
            summary = summarize_incident(incident, event)
            incident.summary = summary
            db.add(incident)
            db.commit()

            print(f"[detect] Created incident {incident.id} for event {event.id}")
