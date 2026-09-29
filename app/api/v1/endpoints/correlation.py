import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import Case
from app.models.entity import EntityMatch, EntityMention
from app.models.evidence import Evidence
from app.models.relationship import Relationship
from app.models.user import User
from app.schemas.correlation import EntityMatchResponse, RelationshipResponse, CorrelationSummaryResponse
from app.services.correlation.pipeline import run_case_correlation_pipeline
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/cases/{case_id}/correlate", response_model=CorrelationSummaryResponse)
def correlate_case_evidence(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers Candidate Entity Matching & Cross-Evidence Correlation Engine for a case:
    1. Evaluates extracted mentions across all evidence files in the case.
    2. Populates `entity_matches` table with candidate matches, confidence ratings, and rationale.
    3. Populates `relationships` table with cross-evidence entity links.
    4. Logs audit entry ('CORRELATION_COMPLETED').
    """
    try:
        matches, relationships = run_case_correlation_pipeline(db, case_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Correlation error: {str(e)}")

    return CorrelationSummaryResponse(
        case_id=case_id,
        total_candidate_matches=len(matches),
        total_relationships=len(relationships),
        matches=matches,
        relationships=relationships
    )

@router.get("/cases/{case_id}/matches", response_model=List[EntityMatchResponse])
def get_case_candidate_matches(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all candidate entity matches discovered within a case.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    # Join EntityMatch via EntityMention -> Evidence -> Case
    matches = (
        db.query(EntityMatch)
        .join(EntityMention, EntityMatch.source_mention_id == EntityMention.id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .all()
    )
    return matches

@router.get("/cases/{case_id}/relationships", response_model=List[RelationshipResponse])
def get_case_relationships(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all cross-evidence entity relationships discovered within a case.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    relationships = db.query(Relationship).filter(Relationship.case_id == case_id).all()
    return relationships

@router.patch("/matches/{match_id}", response_model=EntityMatchResponse)
def update_match_status(
    match_id: uuid.UUID,
    match_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the review status of a candidate entity match ('ACCEPTED', 'REJECTED', 'PENDING_REVIEW').
    """
    match_obj = db.query(EntityMatch).filter(EntityMatch.id == match_id).first()
    if not match_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity match with ID '{match_id}' not found."
        )

    valid_statuses = {"ACCEPTED", "REJECTED", "PENDING_REVIEW"}
    upper_status = match_status.upper()
    if upper_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid match status '{match_status}'. Allowed: {sorted(list(valid_statuses))}"
        )

    match_obj.status = upper_status
    db.add(match_obj)
    db.commit()
    db.refresh(match_obj)
    return match_obj

