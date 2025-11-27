# app/schemas.py
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime

class EventIn(BaseModel):
    source: str = Field(..., description="log source, e.g. 'suricata'")
    host: Optional[str] = Field(None, description="hostname where log was generated")

    # normalized fields (optional, but recommended)
    ts: Optional[datetime] = None
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    proto: Optional[str] = None

    raw: Dict[str, Any] = Field(
        ..., description="original raw event as received from log source"
    )

class EventOut(BaseModel):
    id: int
    source: str
    host: Optional[str]
    ts: datetime
    src_ip: Optional[str]
    dst_ip: Optional[str]
    src_port: Optional[int]
    dst_port: Optional[int]
    proto: Optional[str]
    raw: Dict[str, Any]

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode = True in v1)
