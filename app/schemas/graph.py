from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # 'EVIDENCE' or 'ENTITY'
    category: str  # EMAIL, IP, PERSON, PDF, CHAT, etc.
    val: int = 10
    details: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class GraphLink(BaseModel):
    source: str
    target: str
    label: str
    type: str  # 'CONTAINMENT', 'RELATIONSHIP', 'MATCH'
    confidence: Optional[str] = "HIGH"
    rationale: Optional[str] = None

class GraphResponse(BaseModel):
    case_id: str
    nodes: List[GraphNode]
    links: List[GraphLink]
    total_nodes: int
    total_links: int
