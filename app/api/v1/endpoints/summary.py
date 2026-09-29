import uuid
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention, EntityMatch
from app.models.relationship import Relationship
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.summary import CaseSummaryResponse, AuditLogSummary
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/cases/{case_id}/summary", response_model=CaseSummaryResponse)
def get_case_summary(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns aggregated case investigation summary:
    - Case metadata and status
    - Total count of ingested evidence items
    - Total canonical entities grouped by entity_type (EMAIL, IP, PHONE, PERSON, LOCATION, ACCOUNT)
    - Total cross-evidence relationships
    - Total pending candidate matches
    - Last 10 audit log entries
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    total_evidence = db.query(Evidence).filter(Evidence.case_id == case_id).count()

    type_counts_query = (
        db.query(Entity.entity_type, func.count(func.distinct(Entity.id)))
        .join(EntityMention, Entity.id == EntityMention.entity_id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .group_by(Entity.entity_type)
        .all()
    )
    entities_by_type: Dict[str, int] = {e_type: count for e_type, count in type_counts_query}
    total_entities = sum(entities_by_type.values())

    total_relationships = db.query(Relationship).filter(Relationship.case_id == case_id).count()

    pending_matches = (
        db.query(EntityMatch)
        .join(EntityMention, EntityMatch.source_mention_id == EntityMention.id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id, EntityMatch.status == "PENDING_REVIEW")
        .count()
    )

    recent_logs = (
        db.query(AuditLog, User.username)
        .outerjoin(User, AuditLog.user_id == User.id)
        .filter(AuditLog.case_id == case_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(10)
        .all()
    )

    audit_summaries = []
    for log_obj, username in recent_logs:
        actor_name = username or log_obj.actor or "System"
        audit_summaries.append(
            AuditLogSummary(
                id=log_obj.id,
                action=log_obj.action,
                actor=actor_name,
                details=log_obj.details,
                timestamp=log_obj.timestamp
            )
        )

    return CaseSummaryResponse(
        case_id=case.id,
        case_number=case.case_number,
        title=case.title,
        status=case.status,
        description=case.description,
        total_evidence_items=total_evidence,
        total_canonical_entities=total_entities,
        entities_by_type=entities_by_type,
        total_relationships=total_relationships,
        total_pending_matches=pending_matches,
        recent_audit_logs=audit_summaries
    )
