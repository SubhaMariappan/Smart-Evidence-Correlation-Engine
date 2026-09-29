import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence.id", ondelete="SET NULL"), nullable=True, index=True)
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    case = relationship("Case", back_populates="timeline_events")
    evidence = relationship("Evidence", back_populates="timeline_events")
