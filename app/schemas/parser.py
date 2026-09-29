import uuid
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, ConfigDict

class MetadataEntryResponse(BaseModel):
    key: str
    value: str

    model_config = ConfigDict(from_attributes=True)

class ParseEvidenceResponse(BaseModel):
    evidence_id: uuid.UUID
    original_filename: str
    processing_status: str
    parsed_at: datetime
    text_preview: str
    metadata: Dict[str, str]
