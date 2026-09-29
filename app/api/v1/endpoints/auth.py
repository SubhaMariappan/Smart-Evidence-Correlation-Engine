from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user

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
        role=user_in.role
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
