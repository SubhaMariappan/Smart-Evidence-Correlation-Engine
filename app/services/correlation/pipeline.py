import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.entity import EntityMatch
from app.models.relationship import Relationship
from app.models.audit import AuditLog
from app.services.correlation.matcher import CandidateMatcher
from app.services.correlation.engine import CorrelationEngine

def run_case_correlation_pipeline(db: Session, case_id: uuid.UUID, current_user_id: uuid.UUID) -> Tuple[List[EntityMatch], List[Relationship]]:
    """
    Executes candidate matching and cross-evidence correlation pipeline for a case:
    1. Evaluates extracted mentions across evidence files in the case using CandidateMatcher.
    2. Populates `entity_matches` table.
    3. Triggers CorrelationEngine to discover cross-evidence relationships between entities.
    4. Populates `relationships` table.
    5. Logs `CORRELATION_COMPLETED` audit entry.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise ValueError(f"Case with ID '{case_id}' not found.")

    matcher = CandidateMatcher()
    engine = CorrelationEngine()

    matches = matcher.generate_candidate_matches(db, case_id)
    relationships = engine.generate_case_relationships(db, case_id)

    audit_entry = AuditLog(
        case_id=case_id,
        user_id=current_user_id,
        action="CORRELATION_COMPLETED",
        details=f"Generated {len(matches)} candidate match(es) and {len(relationships)} entity relationship(s) for Case '{case.case_number}'"
    )
    db.add(audit_entry)
    db.commit()

    return matches, relationships
