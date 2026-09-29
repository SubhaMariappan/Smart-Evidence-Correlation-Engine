import os
import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention
from app.models.audit import AuditLog
from app.services.extractors.regex_extractor import RegexExtractor
from app.services.extractors.nlp_extractor import NLPExtractor
from app.services.extractors.normalizer import normalize_entity
from app.services.parsers.factory import ParserFactory

def extract_and_resolve_evidence_entities(db: Session, evidence_id: uuid.UUID, current_user_id: uuid.UUID) -> Tuple[List[EntityMention], List[Entity]]:
    """
    Ingests parsed text from an evidence record, extracts mentions using Regex and NLP extractors,
    normalizes raw values, resolves/creates canonical records in the `entities` table,
    stores occurrences in `entity_mentions`, updates `processing_status` to 'EXTRACTED',
    and logs an audit trail entry.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise ValueError(f"Evidence with ID '{evidence_id}' not found.")

    if not os.path.exists(evidence.storage_path):
        raise ValueError(f"Vault storage error: File not found on disk at '{evidence.storage_path}'.")

    # 1. Parse text using ParserFactory
    parser = ParserFactory.get_parser(evidence.original_filename, evidence.evidence_type)
    parsed_text, _ = parser.parse(evidence.storage_path)

    # 2. Run Extractors
    regex_ext = RegexExtractor()
    nlp_ext = NLPExtractor()

    regex_mentions = regex_ext.extract(parsed_text)
    nlp_mentions = nlp_ext.extract(parsed_text)

    all_raw_mentions = regex_mentions + nlp_mentions

    # Clear previous mentions for this evidence to ensure idempotency
    db.query(EntityMention).filter(EntityMention.evidence_id == evidence_id).delete()

    created_mentions = []
    canonical_entities = {}

    for item in all_raw_mentions:
        raw_val = item["raw_value"]
        e_type = item["entity_type"].upper()
        norm_val = normalize_entity(raw_val, e_type)
        start_off = item["start_offset"]
        end_off = item["end_offset"]

        # Context snippet (50 chars around match)
        start_ctx = max(0, start_off - 25)
        end_ctx = min(len(parsed_text), end_off + 25)
        context_snippet = parsed_text[start_ctx:end_ctx].strip().replace("\n", " ")

        # Canonical Entity resolution: Find or create Entity in `entities` table
        canon_entity = db.query(Entity).filter(
            Entity.entity_type == e_type,
            Entity.canonical_name == norm_val
        ).first()

        if not canon_entity:
            canon_entity = Entity(
                entity_type=e_type,
                canonical_name=norm_val
            )
            db.add(canon_entity)
            db.flush()

        canonical_entities[canon_entity.id] = canon_entity

        # Create EntityMention row
        mention = EntityMention(
            evidence_id=evidence_id,
            entity_id=canon_entity.id,
            entity_type=e_type,
            raw_value=raw_val,
            normalized_value=norm_val,
            context_snippet=context_snippet,
            start_offset=start_off,
            end_offset=end_off
        )
        db.add(mention)
        created_mentions.append(mention)

    # Update evidence processing_status
    evidence.processing_status = "EXTRACTED"
    db.add(evidence)

    # Log Audit Entry
    audit_entry = AuditLog(
        case_id=evidence.case_id,
        user_id=current_user_id,
        action="ENTITIES_EXTRACTED",
        details=f"Extracted {len(created_mentions)} entity mention(s) across {len(canonical_entities)} canonical entity(ies) from '{evidence.original_filename}'"
    )
    db.add(audit_entry)
    db.commit()

    return created_mentions, list(canonical_entities.values())
