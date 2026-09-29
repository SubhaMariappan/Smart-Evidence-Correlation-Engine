import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention
from app.models.user import User
from app.schemas.entity import EntityMentionResponse, CanonicalEntityResponse, ExtractionSummaryResponse
from app.services.extractors.pipeline import extract_and_resolve_evidence_entities
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/evidence/{evidence_id}/extract-entities", response_model=ExtractionSummaryResponse)
def extract_evidence_entities(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers entity extraction & canonical normalization engine:
    1. Extracts mentions using Regex & NLP pattern extractors (EMAIL, PHONE, IP, PERSON, LOCATION, ACCOUNT).
    2. Resolves/creates canonical entities in the `entities` table.
    3. Saves occurrences to `entity_mentions` with context snippets and character offsets.
    4. Updates evidence processing_status to 'EXTRACTED'.
    5. Logs audit entry ('ENTITIES_EXTRACTED').
    """
    try:
        mentions, canonical_list = extract_and_resolve_evidence_entities(db, evidence_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Extraction error: {str(e)}")

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    return ExtractionSummaryResponse(
        evidence_id=evidence.id,
        processing_status=evidence.processing_status,
        total_mentions_extracted=len(mentions),
        distinct_canonical_entities=len(canonical_list),
        mentions=mentions
    )

@router.get("/evidence/{evidence_id}/entities", response_model=List[EntityMentionResponse])
def list_evidence_entity_mentions(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all raw entity mentions extracted from a specific evidence item.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID '{evidence_id}' not found."
        )

    mentions = db.query(EntityMention).filter(EntityMention.evidence_id == evidence_id).all()
    return mentions

@router.get("/cases/{case_id}/entities", response_model=List[CanonicalEntityResponse])
def list_case_canonical_entities(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all distinct canonical entities discovered across all evidence items in a case,
    including total mention count per entity.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    # Query distinct canonical entities linked via entity_mentions -> evidence -> case
    results = (
        db.query(Entity, func.count(EntityMention.id).label("mention_count"))
        .join(EntityMention, Entity.id == EntityMention.entity_id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .group_by(Entity.id)
        .all()
    )

    canonical_responses = []
    for entity_obj, m_count in results:
        resp = CanonicalEntityResponse(
            id=entity_obj.id,
            entity_type=entity_obj.entity_type,
            canonical_name=entity_obj.canonical_name,
            created_at=entity_obj.created_at,
            mention_count=m_count
        )
        canonical_responses.append(resp)

    return canonical_responses
