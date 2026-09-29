import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class CandidateCorrelation(Base):
    __tablename__ = "candidate_correlations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    source_evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence_items.id", ondelete="CASCADE"), nullable=False)
    target_evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence_items.id", ondelete="CASCADE"), nullable=False)
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey("extracted_entities.id", ondelete="CASCADE"), nullable=False)
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey("extracted_entities.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    confidence_score = Column(String(20), nullable=False)
    rationale = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    case = relationship("Case", back_populates="correlations")
