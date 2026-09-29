import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CaseBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Human-readable case title")
    description: Optional[str] = Field(None, description="Detailed case scope and background summary")

class CaseCreate(CaseBase):
    case_number: str = Field(..., min_length=3, max_length=50, description="Unique forensic case number (e.g. SECE-2026-001)")
    status: str = Field("OPEN", description="Initial case status: OPEN, IN_PROGRESS, CLOSED, ARCHIVED")

class CaseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, description="Updated status: OPEN, IN_PROGRESS, CLOSED, ARCHIVED")

class CaseRead(CaseBase):
    id: uuid.UUID
    case_number: str
    status: str
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
