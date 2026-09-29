import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ConfigDict

class AuditLogSummary(BaseModel):
    id: uuid.UUID
    action: str
    actor: str
    details: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class CaseSummaryResponse(BaseModel):
    case_id: uuid.UUID
    case_number: str
    title: str
    status: str
    description: Optional[str] = None
    total_evidence_items: int
    total_canonical_entities: int
    entities_by_type: Dict[str, int]
    total_relationships: int
    total_pending_matches: int
    recent_audit_logs: List[AuditLogSummary]
