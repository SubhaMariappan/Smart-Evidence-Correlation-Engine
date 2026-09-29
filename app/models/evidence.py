import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    evidence_type = Column(String(50), nullable=False)
    sha256_hash = Column(String(64), nullable=False, index=True)
    file_size_bytes = Column(BigInteger, nullable=False)
    imported_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    source_description = Column(Text, nullable=True)
    storage_path = Column(String(500), nullable=False)
    processing_status = Column(String(20), nullable=False, default="PENDING")
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    case = relationship("Case", back_populates="evidence_items")
    created_by = relationship("User", back_populates="imported_evidence")
    metadata_entries = relationship("EvidenceMetadata", back_populates="evidence", cascade="all, delete-orphan")
    entity_mentions = relationship("EntityMention", back_populates="evidence", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEvent", back_populates="evidence")


class EvidenceMetadata(Base):
    __tablename__ = "evidence_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)

    # Relationships
    evidence = relationship("Evidence", back_populates="metadata_entries")
