import uuid
from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    INVESTIGATOR = "INVESTIGATOR"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.INVESTIGATOR

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v):
        if isinstance(v, str):
            v_upper = v.upper().strip()
            if v_upper not in (UserRole.ADMIN.value, UserRole.INVESTIGATOR.value):
                raise ValueError(f"Role '{v}' is unauthorized. Allowed roles are strictly 'ADMIN' or 'INVESTIGATOR'.")
            return UserRole(v_upper)
        if isinstance(v, UserRole):
            return v
        raise ValueError("Invalid role. Allowed roles are strictly 'ADMIN' or 'INVESTIGATOR'.")

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
