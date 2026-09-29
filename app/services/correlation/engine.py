import uuid
from typing import List, Dict, Set
from sqlalchemy.orm import Session
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention
from app.models.relationship import Relationship

class CorrelationEngine:
    """
    Analyzes co-occurrences of canonical entities across evidence records within a case.
    Populates cross-evidence entity relationships in the `relationships` table.
    """
    def generate_case_relationships(self, db: Session, case_id: uuid.UUID) -> List[Relationship]:
        db.query(Relationship).filter(Relationship.case_id == case_id).delete()

        evidence_items = db.query(Evidence).filter(Evidence.case_id == case_id).all()
        if len(evidence_items) < 2:
            return []

        evidence_entities: Dict[uuid.UUID, Set[uuid.UUID]] = {}
        entity_lookup: Dict[uuid.UUID, Entity] = {}

        for ev in evidence_items:
            mentions = db.query(EntityMention).filter(EntityMention.evidence_id == ev.id).all()
            e_set = set()
            for m in mentions:
                if m.entity_id:
                    e_set.add(m.entity_id)
                    if m.entity_id not in entity_lookup:
                        entity_obj = db.query(Entity).filter(Entity.id == m.entity_id).first()
                        if entity_obj:
                            entity_lookup[m.entity_id] = entity_obj
            evidence_entities[ev.id] = e_set

        created_relationships = []
        seen_rel_pairs = set()

        ev_ids = list(evidence_entities.keys())
        for i in range(len(ev_ids)):
            for j in range(i + 1, len(ev_ids)):
                ev1_id = ev_ids[i]
                ev2_id = ev_ids[j]

                set1 = evidence_entities[ev1_id]
                set2 = evidence_entities[ev2_id]

                shared_entity_ids = set1.intersection(set2)

                for shared_id in shared_entity_ids:
                    shared_entity = entity_lookup.get(shared_id)
                    if not shared_entity:
                        continue

                    other_entity_ids = (set1 | set2) - {shared_id}
                    for other_id in other_entity_ids:
                        other_entity = entity_lookup.get(other_id)
                        if not other_entity:
                            continue

                        pair_key = tuple(sorted([str(shared_id), str(other_id)]))
                        if pair_key in seen_rel_pairs:
                            continue
                        seen_rel_pairs.add(pair_key)

                        rel_type = f"SHARED_{shared_entity.entity_type}"
                        rationale = (
                            f"Entity '{shared_entity.canonical_name}' ({shared_entity.entity_type}) "
                            f"co-occurs with '{other_entity.canonical_name}' ({other_entity.entity_type}) "
                            f"across evidence records in Case."
                        )

                        rel_obj = Relationship(
                            case_id=case_id,
                            source_entity_id=shared_id,
                            target_entity_id=other_id,
                            relationship_type=rel_type,
                            confidence_score="HIGH" if shared_entity.entity_type in ['EMAIL', 'PHONE', 'IP'] else "MEDIUM",
                            rationale=rationale
                        )
                        db.add(rel_obj)
                        created_relationships.append(rel_obj)

        db.flush()
        return created_relationships
