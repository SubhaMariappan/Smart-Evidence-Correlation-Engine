import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import Case
from app.models.evidence import Evidence, EvidenceMetadata
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.evidence import EvidenceRead, EvidenceIntegrityResponse
from app.schemas.parser import ParseEvidenceResponse, MetadataEntryResponse
from app.services.hasher import compute_sha256_stream, compute_sha256_filepath
from app.services.storage import save_evidence_file
from app.services.parsers.factory import ParserFactory
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/cases/{case_id}/evidence/upload", response_model=EvidenceRead, status_code=status.HTTP_201_CREATED)
def upload_evidence(
    case_id: uuid.UUID,
    file: UploadFile = File(...),
    evidence_type: str = Form(..., description="EMAIL, CHAT, PDF, FINANCIAL_LOG, BROWSER_LOG, CALL_LOG, OTHER"),
    source_description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ingests a raw forensic evidence file for a specific case:
    1. Verifies parent case existence.
    2. Computes SHA-256 cryptographic digest in streaming 64KB chunks.
    3. Saves raw immutable file into secure vault storage (`storage/evidence_vault/{case_id}/`).
    4. Records provenance metadata into PostgreSQL `evidence` table.
    5. Inserts audit log entry (`EVIDENCE_UPLOADED`).
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    valid_types = {"EMAIL", "CHAT", "PDF", "FINANCIAL_LOG", "BROWSER_LOG", "CALL_LOG", "OTHER"}
    type_upper = evidence_type.upper()
    if type_upper not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid evidence type '{evidence_type}'. Allowed: {sorted(list(valid_types))}"
        )

    sha256_digest, file_size = compute_sha256_stream(file.file)
    relative_storage_path = save_evidence_file(case_id, file.filename, file.file)

    evidence_item = Evidence(
        case_id=case_id,
        original_filename=file.filename,
        evidence_type=type_upper,
        sha256_hash=sha256_digest,
        file_size_bytes=file_size,
        source_description=source_description,
        storage_path=relative_storage_path,
        processing_status="PENDING",
        created_by_id=current_user.id
    )
    db.add(evidence_item)
    db.commit()
    db.refresh(evidence_item)

    audit_entry = AuditLog(
        case_id=case_id,
        user_id=current_user.id,
        action="EVIDENCE_UPLOADED",
        details=f"Uploaded evidence '{file.filename}' ({file_size} bytes, SHA256: {sha256_digest[:16]}...)"
    )
    db.add(audit_entry)
    db.commit()

    return evidence_item

@router.get("/cases/{case_id}/evidence/", response_model=List[EvidenceRead])
def list_case_evidence(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all evidence records associated with a specific forensic case.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )

    evidence_list = db.query(Evidence).filter(Evidence.case_id == case_id).order_by(Evidence.imported_at.desc()).all()
    return evidence_list

@router.post("/evidence/{evidence_id}/verify-integrity", response_model=EvidenceIntegrityResponse)
def verify_evidence_integrity(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Re-calculates disk file SHA-256 digest and compares against stored hash to verify integrity.
    Detects any unauthorized modification or file tampering.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID '{evidence_id}' not found."
        )

    if not os.path.exists(evidence.storage_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vault storage error: File not found on disk at '{evidence.storage_path}'."
        )

    calculated_hash, _ = compute_sha256_filepath(evidence.storage_path)
    is_valid = (calculated_hash.lower() == evidence.sha256_hash.lower())

    audit_entry = AuditLog(
        case_id=evidence.case_id,
        user_id=current_user.id,
        action="EVIDENCE_INTEGRITY_VERIFIED",
        details=f"Integrity check for '{evidence.original_filename}': Result={'PASS' if is_valid else 'FAIL (TAMPERED)'}"
    )
    db.add(audit_entry)
    db.commit()

    return EvidenceIntegrityResponse(
        evidence_id=evidence.id,
        original_filename=evidence.original_filename,
        stored_sha256_hash=evidence.sha256_hash,
        calculated_sha256_hash=calculated_hash,
        is_valid=is_valid,
        verified_at=datetime.now(timezone.utc)
    )

@router.post("/evidence/{evidence_id}/parse", response_model=ParseEvidenceResponse)
def parse_evidence(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers modular evidence parsing engine:
    1. Locates stored file on disk.
    2. Selects appropriate parser via ParserFactory (Text, CSV, PDF).
    3. Extracts text and technical metadata.
    4. Saves extracted key-value entries to `evidence_metadata` table.
    5. Updates evidence processing_status to 'PARSED'.
    6. Logs audit trail entry ('EVIDENCE_PARSED').
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID '{evidence_id}' not found."
        )

    if not os.path.exists(evidence.storage_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vault storage error: File not found on disk at '{evidence.storage_path}'."
        )

    parser = ParserFactory.get_parser(evidence.original_filename, evidence.evidence_type)
    try:
        parsed_text, metadata_dict = parser.parse(evidence.storage_path)
    except Exception as e:
        evidence.processing_status = "ERROR"
        db.add(evidence)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Parsing error: Failed to parse file content ({str(e)})"
        )

    # Save extracted metadata entries in database
    db.query(EvidenceMetadata).filter(EvidenceMetadata.evidence_id == evidence_id).delete()
    
    for k, v in metadata_dict.items():
        meta_entry = EvidenceMetadata(
            evidence_id=evidence_id,
            key=str(k),
            value=str(v)
        )
        db.add(meta_entry)

    evidence.processing_status = "PARSED"
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    audit_entry = AuditLog(
        case_id=evidence.case_id,
        user_id=current_user.id,
        action="EVIDENCE_PARSED",
        details=f"Parsed evidence '{evidence.original_filename}' using {metadata_dict.get('parser', 'Parser')}"
    )
    db.add(audit_entry)
    db.commit()

    text_preview = parsed_text[:500] + ("..." if len(parsed_text) > 500 else "")

    return ParseEvidenceResponse(
        evidence_id=evidence.id,
        original_filename=evidence.original_filename,
        processing_status=evidence.processing_status,
        parsed_at=datetime.now(timezone.utc),
        text_preview=text_preview,
        metadata={str(k): str(v) for k, v in metadata_dict.items()}
    )

@router.get("/evidence/{evidence_id}/metadata", response_model=List[MetadataEntryResponse])
def get_evidence_metadata(
    evidence_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves stored technical metadata entries for a specific evidence item.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID '{evidence_id}' not found."
        )

    metadata_list = db.query(EvidenceMetadata).filter(EvidenceMetadata.evidence_id == evidence_id).all()
    return metadata_list
