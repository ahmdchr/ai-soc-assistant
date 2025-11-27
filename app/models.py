# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from .db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)          # "suricata" | "zeek" | "cowrie" | "manual"
    host = Column(String, index=True, nullable=True)

    ts = Column(DateTime, server_default=func.now())  # event timestamp

    src_ip = Column(String, index=True, nullable=True)
    dst_ip = Column(String, index=True, nullable=True)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, nullable=True)
    proto = Column(String, nullable=True)        # tcp/udp/icmp/etc.

    raw = Column(JSON)                           # original data (full log/event)


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    severity = Column(String, default="low")
    status = Column(String, default="open")
    created_at = Column(DateTime, server_default=func.now())
    summary = Column(String, nullable=True)
    data = Column(JSON, nullable=True)
    acknowledged = Column(Boolean, default=False)
    technique = Column(String, nullable=True)   # MITRE ATT&CK id(s), e.g. "T1071.001"
