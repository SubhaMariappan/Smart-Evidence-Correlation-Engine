import hashlib
from typing import BinaryIO, Tuple

def compute_sha256_stream(file_obj: BinaryIO, chunk_size: int = 65536) -> Tuple[str, int]:
    """
    Computes cryptographic SHA-256 digest and total file size in bytes
    by reading a file object in 64KB (65536 bytes) streaming chunks.
    """
    sha256 = hashlib.sha256()
    total_bytes = 0
    file_obj.seek(0)
    
    while chunk := file_obj.read(chunk_size):
        sha256.update(chunk)
        total_bytes += len(chunk)
        
    file_obj.seek(0)
    return sha256.hexdigest(), total_bytes

def compute_sha256_filepath(file_path: str, chunk_size: int = 65536) -> Tuple[str, int]:
    """
    Computes cryptographic SHA-256 digest and total file size in bytes for a file stored on disk.
    """
    sha256 = hashlib.sha256()
    total_bytes = 0
    
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
            total_bytes += len(chunk)
            
    return sha256.hexdigest(), total_bytes
