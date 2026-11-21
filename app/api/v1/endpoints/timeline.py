import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.timeline import TimelineEvent
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.timeline import TimelineEventResponse, TimelineEventCreate
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/cases/{case_id}/timeline", response_model=List[TimelineEventResponse])
def get_case_timeline(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reconstructs chronological forensic event timeline for an active case investigation.
    Combines parsed document timestamps, evidence ingestion dates, and audit milestones.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    # 1. Fetch recorded timeline events
    events = (
        db.query(TimelineEvent, Evidence.original_filename)
        .outerjoin(Evidence, TimelineEvent.evidence_id == Evidence.id)
        .filter(TimelineEvent.case_id == case_id)
        .order_by(asc(TimelineEvent.event_timestamp))
        .all()
    )

    results = []
    seen_ids = set()

    for event_obj, filename in events:
        seen_ids.add(event_obj.id)
        results.append(TimelineEventResponse(
            id=event_obj.id,
            case_id=event_obj.case_id,
            evidence_id=event_obj.evidence_id,
            evidence_filename=filename,
            event_timestamp=event_obj.event_timestamp,
            title=event_obj.title,
            description=event_obj.description,
            event_type=event_obj.event_type or "EVENT",
            created_at=event_obj.created_at
        ))

    # 2. If events are sparse, synthesize baseline milestone events from imported evidence
    if len(results) == 0:
        evidence_items = db.query(Evidence).filter(Evidence.case_id == case_id).order_by(asc(Evidence.imported_at)).all()
        for ev in evidence_items:
            # Create persistent ingestion milestone
            ingest_event = TimelineEvent(
                case_id=case_id,
                evidence_id=ev.id,
                event_timestamp=ev.imported_at,
                title=f"Evidence Vault Intake: {ev.original_filename}",
                description=f"File ingested ({ev.file_size_bytes} bytes). SHA-256 Digest: {ev.sha256_hash[:16]}...",
                event_type="INGESTION"
            )
            db.add(ingest_event)
            db.commit()
            db.refresh(ingest_event)

            results.append(TimelineEventResponse(
                id=ingest_event.id,
                case_id=ingest_event.case_id,
                evidence_id=ingest_event.evidence_id,
                evidence_filename=ev.original_filename,
                event_timestamp=ingest_event.event_timestamp,
                title=ingest_event.title,
                description=ingest_event.description,
                event_type=ingest_event.event_type,
                created_at=ingest_event.created_at
            ))

    return results

@router.post("/cases/{case_id}/timeline", response_model=TimelineEventResponse, status_code=status.HTTP_201_CREATED)
def create_custom_timeline_event(
    case_id: uuid.UUID,
    event_in: TimelineEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows an investigator to append a custom timeline annotation or milestone.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    new_event = TimelineEvent(
        case_id=case_id,
        evidence_id=event_in.evidence_id,
        event_timestamp=event_in.event_timestamp,
        title=event_in.title,
        description=event_in.description,
        event_type=event_in.event_type or "INVESTIGATOR_NOTE"
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    filename = None
    if event_in.evidence_id:
        ev = db.query(Evidence).filter(Evidence.id == event_in.evidence_id).first()
        filename = ev.original_filename if ev else None

    # Audit log
    audit = AuditLog(
        case_id=case_id,
        user_id=current_user.id,
        action="TIMELINE_EVENT_ADDED",
        details=f"Added timeline milestone: '{new_event.title}'"
    )
    db.add(audit)
    db.commit()

    return TimelineEventResponse(
        id=new_event.id,
        case_id=new_event.case_id,
        evidence_id=new_event.evidence_id,
        evidence_filename=filename,
        event_timestamp=new_event.event_timestamp,
        title=new_event.title,
        description=new_event.description,
        event_type=new_event.event_type,
        created_at=new_event.created_at
    )
