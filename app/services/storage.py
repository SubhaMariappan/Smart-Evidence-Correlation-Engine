import os
import re
import uuid
import shutil
from typing import BinaryIO
from fastapi import HTTPException, status
from app.core.config import settings

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes raw uploaded filename to prevent directory traversal attacks (e.g., ../../etc/passwd)
    and removes special characters that cause filesystem errors.
    """
    basename = os.path.basename(filename)
    clean_name = re.sub(r'[^a-zA-Z0-9._-]', '_', basename)
    clean_name = clean_name.lstrip('.')
    if not clean_name:
        clean_name = f"evidence_{uuid.uuid4().hex[:8]}.bin"
    return clean_name

def save_evidence_file(case_id: uuid.UUID, filename: str, file_obj: BinaryIO) -> str:
    """
    Saves an uploaded file to the secure evidence vault repository:
    `storage/evidence_vault/{case_id}/{unique_prefix}_{clean_filename}`
    Returns the sanitized relative storage path.
    """
    clean_name = sanitize_filename(filename)
    
    case_vault_dir = os.path.join(settings.STORAGE_VAULT_DIR, str(case_id))
    os.makedirs(case_vault_dir, exist_ok=True)
    
    unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_name}"
    target_full_path = os.path.join(case_vault_dir, unique_filename)
    
    # Path Traversal Guard: Ensure target path strictly remains inside vault directory
    abs_vault = os.path.abspath(settings.STORAGE_VAULT_DIR)
    abs_target = os.path.abspath(target_full_path)
    if not abs_target.startswith(abs_vault):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Security error: Invalid file path traversal attempt detected."
        )

    file_obj.seek(0)
    with open(target_full_path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)
        
    relative_path = os.path.relpath(target_full_path, start=".").replace("\\", "/")
    return relative_path
