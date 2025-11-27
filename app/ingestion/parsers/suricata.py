# app/ingestion/parsers/suricata.py
from typing import Dict, Any, Optional

def normalize_suricata_event(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a Suricata EVE.json event into our normalized schema for EventIn.
    This is a basic v1; you can enrich it later.
    """
    src_ip = raw.get("src_ip")
    dst_ip = raw.get("dst_ip")
    src_port = raw.get("src_port")
    dst_port = raw.get("dst_port")
    proto = raw.get("proto")

    host = raw.get("host")  # sometimes available, sometimes not

    normalized = {
        "source": "suricata",
        "host": host,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "proto": proto,
        "raw": raw,
    }

    return normalized
