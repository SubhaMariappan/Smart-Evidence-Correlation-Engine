import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.entity import EntityMentionResponse

class EvidenceBase(BaseModel):
    original_filename: str
    evidence_type: str = Field(..., description="Category: EMAIL, CHAT, PDF, FINANCIAL_LOG, BROWSER_LOG, CALL_LOG, OTHER")
    source_description: Optional[str] = None

class EvidenceRead(EvidenceBase):
    id: uuid.UUID
    case_id: uuid.UUID
    sha256_hash: str
    file_size_bytes: int
    imported_at: datetime
    storage_path: str
    processing_status: str
    created_by_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

class EvidenceIntegrityResponse(BaseModel):
    evidence_id: uuid.UUID
    original_filename: str
    stored_sha256_hash: str
    calculated_sha256_hash: str
    is_valid: bool
    verified_at: datetime

class EvidenceContentResponse(BaseModel):
    evidence_id: uuid.UUID
    case_id: uuid.UUID
    original_filename: str
    evidence_type: str
    file_size_bytes: int
    sha256_hash: str
    processing_status: str
    source_description: Optional[str] = None
    parsed_text: str
    metadata: Dict[str, str] = {}
    mentions: List[EntityMentionResponse] = []
