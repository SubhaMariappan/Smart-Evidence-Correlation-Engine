import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="OPEN")
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    created_by = relationship("User", back_populates="created_cases")
    evidence_items = relationship("Evidence", back_populates="case", cascade="all, delete-orphan")
    relationships = relationship("Relationship", back_populates="case", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEvent", back_populates="case", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="case")
