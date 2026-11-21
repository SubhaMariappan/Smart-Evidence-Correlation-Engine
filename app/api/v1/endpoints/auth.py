import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user, require_role, require_any_role

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new investigator or analyst user account.
    Hashes password securely with bcrypt and stores in PostgreSQL users table.
    """
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )

    # Create user with bcrypt password hash
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role.value if hasattr(user_in.role, 'value') else str(user_in.role)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Audit log entry
    audit_entry = AuditLog(
        user_id=new_user.id,
        action="USER_REGISTERED",
        details=f"Registered user '{new_user.username}' with role '{new_user.role}'"
    )
    db.add(audit_entry)
    db.commit()

    return new_user

@router.post("/login", response_model=Token)
def login_json(login_in: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user via JSON body and return a signed JWT access token.
    """
    user = db.query(User).filter(User.username == login_in.username).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    access_token = create_access_token(subject=user.username)
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login/token", response_model=Token)
def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login endpoint for Swagger UI (/docs) Authorization button.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    access_token = create_access_token(subject=user.username)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Protected endpoint: Returns information about the currently authenticated user.
    """
    return current_user

@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role("ADMIN"))
):
    """
    Administrative endpoint: List all registered investigator and admin user accounts.
    Strictly forbidden for INVESTIGATOR role.
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users

@router.patch("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: uuid.UUID,
    is_active: bool,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role("ADMIN"))
):
    """
    Administrative endpoint: Activate or deactivate a user account.
    Strictly forbidden for INVESTIGATOR role.
    """
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")
    
    target_user.is_active = is_active
    db.add(target_user)
    
    # Audit logging
    audit_entry = AuditLog(
        user_id=admin_user.id,
        action="USER_STATUS_UPDATED",
        details=f"Admin '{admin_user.username}' changed user '{target_user.username}' status to active={is_active}"
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(target_user)
    return target_user

@router.get("/audit-all")
def get_system_audit_logs(
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role("ADMIN"))
):
    """
    Administrative endpoint: Inspect system-wide immutable Chain of Custody audit logs.
    Strictly forbidden for INVESTIGATOR role.
    """
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": str(log.id),
            "case_id": str(log.case_id) if log.case_id else None,
            "user_id": str(log.user_id) if log.user_id else None,
            "actor": log.user.username if log.user else "System",
            "action": log.action,
            "details": log.details,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]
