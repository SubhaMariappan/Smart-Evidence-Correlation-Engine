import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "INVESTIGATOR"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
