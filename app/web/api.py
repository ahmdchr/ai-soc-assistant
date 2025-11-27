# app/web/api.py
from fastapi import FastAPI, HTTPException
from typing import List

from ..db import Base, engine, SessionLocal
from ..models import Event, Incident
from ..schemas import EventIn, EventOut
from ..detect.rules import run_detection_pipeline

# Create tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adaptive SOC Assistant", version="0.3.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "adaptive-soc-assistant"}


@app.post("/ingest", response_model=EventOut)
def ingest_event(event: EventIn):
    """
    Phase 3: store event in DB, then run detection rules.
    """
    if not event.source:
        raise HTTPException(status_code=400, detail="source is required")

    with SessionLocal() as db:
        obj = Event(
            source=event.source,
            host=event.host,
            ts=event.ts,  # can be None → DB default
            src_ip=event.src_ip,
            dst_ip=event.dst_ip,
            src_port=event.src_port,
            dst_port=event.dst_port,
            proto=event.proto,
            raw=event.raw,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)

        # 🔥 Run detection on this event
        run_detection_pipeline(db, obj)

        return obj


@app.get("/events", response_model=List[EventOut])
def list_events(limit: int = 50):
    with SessionLocal() as db:
        rows = (
            db.query(Event)
            .order_by(Event.id.desc())
            .limit(limit)
            .all()
        )
        return rows


@app.get("/incidents")
def list_incidents(limit: int = 50):
    """
    Simple incidents list (JSON).
    """
    with SessionLocal() as db:
        rows = (
            db.query(Incident)
            .order_by(Incident.id.desc())
            .limit(limit)
            .all()
        )
        # For now, return raw dicts
        return [
            {
                "id": i.id,
                "title": i.title,
                "severity": i.severity,
                "status": i.status,
                "technique": getattr(i, "technique", ""),
                "data": i.data,
                "created_at": i.created_at,
                "summary": i.summary,
            }
            for i in rows
        ]


@app.get("/")
def root():
    return {
        "message": "Adaptive SOC Assistant API",
        "endpoints": ["/health", "/ingest", "/events", "/incidents"],
    }

