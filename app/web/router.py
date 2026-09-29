import uuid
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.entity import Entity, EntityMention, EntityMatch
from app.models.relationship import Relationship
from app.api.v1.endpoints.summary import get_case_summary

templates = Jinja2Templates(directory="app/templates")

web_router = APIRouter()

@web_router.get("/", response_class=RedirectResponse)
def root_redirect():
    """Redirect root access to login page."""
    return RedirectResponse(url="/login")

@web_router.get("/login", response_class=HTMLResponse)
def render_login_page(request: Request):
    """Render modern forensic workstation login view."""
    return templates.TemplateResponse(request=request, name="login.html")

@web_router.get("/app", response_class=HTMLResponse)
def render_app_workspace(request: Request):
    """Render unified forensic application workspace shell."""
    return templates.TemplateResponse(request=request, name="app.html")

@web_router.get("/investigation/{case_id}", response_class=HTMLResponse)
def render_case_investigation_view(request: Request, case_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Legacy case investigation view mapping.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    class SystemUser:
        id = case.created_by_id or uuid.uuid4()
        username = "Investigator"

    summary_data = get_case_summary(case_id=case_id, db=db, current_user=SystemUser())

    evidence_list = db.query(Evidence).filter(Evidence.case_id == case_id).all()
    
    canonical_list = (
        db.query(Entity.entity_type, Entity.canonical_name, func.count(EntityMention.id).label("mention_count"))
        .join(EntityMention, Entity.id == EntityMention.entity_id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .group_by(Entity.id)
        .all()
    )

    canonical_objs = [
        {"entity_type": e_type, "canonical_name": c_name, "mention_count": m_count}
        for e_type, c_name, m_count in canonical_list
    ]

    matches_list = (
        db.query(EntityMatch)
        .join(EntityMention, EntityMatch.source_mention_id == EntityMention.id)
        .join(Evidence, EntityMention.evidence_id == Evidence.id)
        .filter(Evidence.case_id == case_id)
        .all()
    )

    relationships_list = db.query(Relationship).filter(Relationship.case_id == case_id).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "summary": summary_data,
            "evidence_list": evidence_list,
            "canonical_list": canonical_objs,
            "matches_list": matches_list,
            "relationships_list": relationships_list,
            "str": str
        }
    )

@web_router.get("/dashboard", response_class=RedirectResponse)
def render_dashboard_overview():
    """
    Redirect legacy /dashboard to unified /app.
    """
    return RedirectResponse(url="/app")

