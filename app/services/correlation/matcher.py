import uuid
from typing import List, Tuple, Optional
from difflib import SequenceMatcher
from sqlalchemy.orm import Session
from app.models.evidence import Evidence
from app.models.entity import EntityMention, EntityMatch

class CandidateMatcher:
    """
    Evaluates pairs of extracted entity mentions across different evidence items within a case.
    Populates candidate matches with confidence scores and match rationale.
    """
    def generate_candidate_matches(self, db: Session, case_id: uuid.UUID) -> List[EntityMatch]:
        evidence_ids = [e.id for e in db.query(Evidence.id).filter(Evidence.case_id == case_id).all()]
        if not evidence_ids:
            return []

        mentions = db.query(EntityMention).filter(EntityMention.evidence_id.in_(evidence_ids)).all()
        
        mention_ids = [m.id for m in mentions]
        if mention_ids:
            db.query(EntityMatch).filter(
                (EntityMatch.source_mention_id.in_(mention_ids)) | 
                (EntityMatch.target_mention_id.in_(mention_ids))
            ).delete(synchronize_session=False)

        created_matches = []
        seen_pairs = set()

        for i in range(len(mentions)):
            for j in range(i + 1, len(mentions)):
                m1 = mentions[i]
                m2 = mentions[j]

                # Only evaluate mentions from DIFFERENT evidence items
                if m1.evidence_id == m2.evidence_id:
                    continue

                pair_key = tuple(sorted([str(m1.id), str(m2.id)]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                confidence, rationale = self._evaluate_match(m1, m2)
                if confidence:
                    match_obj = EntityMatch(
                        source_mention_id=m1.id,
                        target_mention_id=m2.id,
                        confidence_score=confidence,
                        match_rationale=rationale,
                        status="PENDING_REVIEW"
                    )
                    db.add(match_obj)
                    created_matches.append(match_obj)

        db.flush()
        return created_matches

    def _evaluate_match(self, m1: EntityMention, m2: EntityMention) -> Tuple[Optional[str], Optional[str]]:
        # 1. Deterministic Identifiers (EMAIL, PHONE, IP, ACCOUNT, URL)
        if m1.entity_type == m2.entity_type and m1.entity_type in ['EMAIL', 'PHONE', 'IP', 'ACCOUNT', 'URL']:
            if m1.normalized_value == m2.normalized_value:
                return "HIGH", f"Exact match on {m1.entity_type} '{m1.normalized_value}' across Evidence A and Evidence B"

        # 2. Person Name Similarity
        if m1.entity_type == 'PERSON' and m2.entity_type == 'PERSON':
            val1 = m1.normalized_value
            val2 = m2.normalized_value

            if val1 == val2:
                return "HIGH", f"Exact match on Person name '{val1}' across Evidence A and Evidence B"

            if (val1 in val2 or val2 in val1) and min(len(val1), len(val2)) >= 3:
                return "MEDIUM", f"Partial name match between '{val1}' and '{val2}'"

            ratio = SequenceMatcher(None, val1, val2).ratio()
            if ratio >= 0.8:
                return "MEDIUM", f"Name fuzzy similarity ({int(ratio*100)}%) between '{val1}' and '{val2}'"

        return None, None
