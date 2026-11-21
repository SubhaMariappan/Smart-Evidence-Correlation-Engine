import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention, EntityMatch
from app.models.relationship import Relationship
from app.models.user import User
from app.schemas.graph import GraphResponse, GraphNode, GraphLink
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/cases/{case_id}/graph", response_model=GraphResponse)
def get_case_relationship_graph(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Constructs an interactive node-link graph for an active case:
    - Nodes: Evidence vault files and discovered Canonical Entities.
    - Edges: Containment links, Cross-evidence relationships, and Candidate matches.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    nodes: List[GraphNode] = []
    links: List[GraphLink] = []
    seen_nodes = set()
    seen_links = set()

    # 1. Evidence Nodes
    evidence_items = db.query(Evidence).filter(Evidence.case_id == case_id).all()
    for ev in evidence_items:
        node_id = f"ev_{ev.id}"
        seen_nodes.add(node_id)
        nodes.append(GraphNode(
            id=node_id,
            label=ev.original_filename,
            type="EVIDENCE",
            category=ev.evidence_type,
            val=18,
            details=f"Type: {ev.evidence_type} | Size: {round(ev.file_size_bytes/1024, 1)} KB | SHA256: {ev.sha256_hash[:12]}..."
        ))

    # 2. Entity Nodes and Containment Edges (Evidence -> Entity)
    mention_records = (
        db.query(
            Entity.id,
            Entity.entity_type,
            Entity.canonical_name,
            EntityMention.evidence_id,
            func.count(EntityMention.id).label("mention_count")
        )
        .join(EntityMention, Entity.id == EntityMention.entity_id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .group_by(Entity.id, Entity.entity_type, Entity.canonical_name, EntityMention.evidence_id)
        .all()
    )

    for ent_id, ent_type, canon_name, ev_id, m_count in mention_records:
        ent_node_id = f"ent_{ent_id}"
        if ent_node_id not in seen_nodes:
            seen_nodes.add(ent_node_id)
            nodes.append(GraphNode(
                id=ent_node_id,
                label=canon_name,
                type="ENTITY",
                category=ent_type,
                val=12 + min(m_count * 2, 20),
                details=f"Type: {ent_type} | Canonical: {canon_name}"
            ))

        # Containment Edge: Evidence -> Entity
        ev_node_id = f"ev_{ev_id}"
        link_key = (ev_node_id, ent_node_id, "CONTAINS")
        if link_key not in seen_links:
            seen_links.add(link_key)
            links.append(GraphLink(
                source=ev_node_id,
                target=ent_node_id,
                label="CONTAINS",
                type="CONTAINMENT",
                confidence="100%",
                rationale=f"Found {m_count} mention(s) in evidence"
            ))

    # 3. Discovered Cross-Evidence Relationships (Entity <-> Entity)
    relationships = db.query(Relationship).filter(Relationship.case_id == case_id).all()
    for rel in relationships:
        src_id = f"ent_{rel.source_entity_id}"
        tgt_id = f"ent_{rel.target_entity_id}"

        # Ensure both nodes exist before linking
        if src_id in seen_nodes and tgt_id in seen_nodes:
            link_key = tuple(sorted([src_id, tgt_id]) + [rel.relationship_type])
            if link_key not in seen_links:
                seen_links.add(link_key)
                links.append(GraphLink(
                    source=src_id,
                    target=tgt_id,
                    label=rel.relationship_type.replace("SHARED_", ""),
                    type="RELATIONSHIP",
                    confidence=rel.confidence_score,
                    rationale=rel.rationale
                ))

    # 4. Candidate Matches
    matches = (
        db.query(EntityMatch)
        .join(EntityMention, EntityMatch.source_mention_id == EntityMention.id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .all()
    )

    for m in matches:
        m1 = db.query(EntityMention).filter(EntityMention.id == m.source_mention_id).first()
        m2 = db.query(EntityMention).filter(EntityMention.id == m.target_mention_id).first()
        if m1 and m2 and m1.entity_id and m2.entity_id:
            src_id = f"ent_{m1.entity_id}"
            tgt_id = f"ent_{m2.entity_id}"
            if src_id in seen_nodes and tgt_id in seen_nodes and src_id != tgt_id:
                link_key = tuple(sorted([src_id, tgt_id]) + ["MATCH"])
                if link_key not in seen_links:
                    seen_links.add(link_key)
                    links.append(GraphLink(
                        source=src_id,
                        target=tgt_id,
                        label=f"MATCH ({m.status})",
                        type="MATCH",
                        confidence=m.confidence_score,
                        rationale=m.match_rationale
                    ))

    return GraphResponse(
        case_id=str(case_id),
        nodes=nodes,
        links=links,
        total_nodes=len(nodes),
        total_links=len(links)
    )
