from typing import Tuple, Dict, Any
from pypdf import PdfReader
from app.services.parsers.base import BaseParser

class PDFParser(BaseParser):
    """
    Parser for PDF documents (.pdf). Extracts page text and PDF document metadata.
    """
    def parse(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        reader = PdfReader(file_path)
        page_texts = []
        
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            page_texts.append(f"--- Page {idx + 1} ---\n{text}")

        full_text = "\n\n".join(page_texts)
        pdf_info = reader.metadata or {}

        metadata = {
            "parser": "PDFParser",
            "page_count": str(len(reader.pages)),
            "title": str(pdf_info.title or ""),
            "author": str(pdf_info.author or ""),
            "creator": str(pdf_info.creator or ""),
            "producer": str(pdf_info.producer or "")
        }

        return full_text, metadata
