import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import Case
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.case import CaseCreate, CaseUpdate, CaseRead
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(
    case_in: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new forensic case container.
    Authenticated investigator is automatically assigned as created_by_id.
    """
    # Check if case_number already exists
    existing_case = db.query(Case).filter(Case.case_number == case_in.case_number).first()
    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Case number '{case_in.case_number}' already exists."
        )

    # Valid status options
    valid_statuses = {"OPEN", "IN_PROGRESS", "CLOSED", "ARCHIVED"}
    status_upper = case_in.status.upper()
    if status_upper not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{case_in.status}'. Allowed: {sorted(list(valid_statuses))}"
        )

    new_case = Case(
        case_number=case_in.case_number,
        title=case_in.title,
        description=case_in.description,
        status=status_upper,
        created_by_id=current_user.id
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # Log audit entry
    audit_entry = AuditLog(
        case_id=new_case.id,
        user_id=current_user.id,
        action="CASE_CREATED",
        details=f"Created case '{new_case.case_number}' ({new_case.title}) with status '{new_case.status}'"
    )
    db.add(audit_entry)
    db.commit()

    return new_case

@router.get("/", response_model=List[CaseRead])
def list_cases(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter cases by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List forensic cases with optional status filtering (OPEN, IN_PROGRESS, CLOSED, ARCHIVED).
    """
    query = db.query(Case)
    if status_filter:
        query = query.filter(Case.status == status_filter.upper())
    
    cases = query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    return cases

@router.get("/{case_id}", response_model=CaseRead)
def get_case(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve detailed forensic case information by UUID.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )
    return case

@router.patch("/{case_id}", response_model=CaseRead)
def update_case(
    case_id: uuid.UUID,
    case_in: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update case details or status. Logs audit entry when status changes.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    old_status = case.status
    update_data = case_in.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"]:
        new_status = update_data["status"].upper()
        valid_statuses = {"OPEN", "IN_PROGRESS", "CLOSED", "ARCHIVED"}
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status '{update_data['status']}'. Allowed: {sorted(list(valid_statuses))}"
            )
        update_data["status"] = new_status

    for field, value in update_data.items():
        setattr(case, field, value)

    db.add(case)
    db.commit()
    db.refresh(case)

    # Log audit entry if status changed
    if "status" in update_data and old_status != case.status:
        audit_entry = AuditLog(
            case_id=case.id,
            user_id=current_user.id,
            action="CASE_STATUS_UPDATED",
            details=f"Case '{case.case_number}' status updated from '{old_status}' to '{case.status}'"
        )
        db.add(audit_entry)
        db.commit()

    return case
