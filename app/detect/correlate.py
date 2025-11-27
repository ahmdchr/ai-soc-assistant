# app/detect/correlate.py
from typing import Dict, Any
from ..models import Event

def get_suricata_severity(event: Event) -> int | None:
    """
    Extract Suricata alert severity from event.raw.
    Suricata EVE.json format usually has: raw["alert"]["severity"].
    """
    raw = event.raw or {}
    alert = raw.get("alert", {})
    sev = alert.get("severity")
    try:
        return int(sev) if sev is not None else None
    except (ValueError, TypeError):
        return None


def rule_matches(rule: Dict[str, Any], event: Event) -> bool:
    """
    Very simple matching logic for now:
    - Rule specifies source (e.g. 'suricata')
    - Rule specifies min_severity for Suricata alerts
    """
    expected_source = rule.get("source")
    if expected_source and event.source != expected_source:
        return False

    # Only Suricata for now
    if expected_source == "suricata":
        min_sev = rule.get("min_severity")
        if min_sev is not None:
            sev = get_suricata_severity(event)
            # Suricata: 1 = highest, 4 = low
            if sev is None:
                return False
            if sev <= int(min_sev):
                return True
            return False

    # If no specific logic, no match
    return False
