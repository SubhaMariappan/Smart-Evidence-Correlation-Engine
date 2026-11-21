import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TimelineEventBase(BaseModel):
    event_timestamp: datetime
    title: str
    description: Optional[str] = None
    event_type: Optional[str] = Field("EVENT", description="INGESTION, PARSED, EXTRACTED, COMMUNICATION, TRANSACTION, ACCESS, AUDIT")

class TimelineEventCreate(TimelineEventBase):
    case_id: uuid.UUID
    evidence_id: Optional[uuid.UUID] = None

class TimelineEventResponse(TimelineEventBase):
    id: uuid.UUID
    case_id: uuid.UUID
    evidence_id: Optional[uuid.UUID] = None
    evidence_filename: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
