import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Entity(Base):
    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False, index=True)
    canonical_name = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    mentions = relationship("EntityMention", back_populates="entity")


class EntityMention(Base):
    __tablename__ = "entity_mentions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="SET NULL"), nullable=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    raw_value = Column(Text, nullable=False)
    normalized_value = Column(Text, nullable=False, index=True)
    context_snippet = Column(Text, nullable=True)
    start_offset = Column(Integer, nullable=True)
    end_offset = Column(Integer, nullable=True)
    extracted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    evidence = relationship("Evidence", back_populates="entity_mentions")
    entity = relationship("Entity", back_populates="mentions")


class EntityMatch(Base):
    __tablename__ = "entity_matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_mention_id = Column(UUID(as_uuid=True), ForeignKey("entity_mentions.id", ondelete="CASCADE"), nullable=False, index=True)
    target_mention_id = Column(UUID(as_uuid=True), ForeignKey("entity_mentions.id", ondelete="CASCADE"), nullable=False, index=True)
    confidence_score = Column(String(20), nullable=False)
    match_rationale = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="PENDING_REVIEW")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
