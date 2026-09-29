import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from jose import jwt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a raw plain text password against a stored bcrypt hash.
    Direct bcrypt execution for high performance & Python 3.14 compatibility.
    """
    pwd_bytes = plain_password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

def get_password_hash(password: str) -> str:
    """
    Generates a secure cryptographic bcrypt hash with salt for a user password.
    Direct bcrypt execution for high performance & Python 3.14 compatibility.
    """
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JSON Web Token (JWT) with expiration time and subject payload.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
