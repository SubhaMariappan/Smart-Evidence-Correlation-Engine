import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class EntityMentionResponse(BaseModel):
    id: uuid.UUID
    evidence_id: uuid.UUID
    entity_id: Optional[uuid.UUID] = None
    entity_type: str
    raw_value: str
    normalized_value: str
    context_snippet: Optional[str] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None
    extracted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CanonicalEntityResponse(BaseModel):
    id: uuid.UUID
    entity_type: str
    canonical_name: str
    created_at: datetime
    mention_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class ExtractionSummaryResponse(BaseModel):
    evidence_id: uuid.UUID
    processing_status: str
    total_mentions_extracted: int
    distinct_canonical_entities: int
    mentions: List[EntityMentionResponse]
