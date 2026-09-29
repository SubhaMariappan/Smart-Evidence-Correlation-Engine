import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

class EntityMatchResponse(BaseModel):
    id: uuid.UUID
    source_mention_id: uuid.UUID
    target_mention_id: uuid.UUID
    confidence_score: str
    match_rationale: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RelationshipResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    source_entity_id: uuid.UUID
    target_entity_id: uuid.UUID
    relationship_type: str
    confidence_score: str
    rationale: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CorrelationSummaryResponse(BaseModel):
    case_id: uuid.UUID
    total_candidate_matches: int
    total_relationships: int
    matches: List[EntityMatchResponse]
    relationships: List[RelationshipResponse]
