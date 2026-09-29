from typing import Tuple, Dict, Any
from app.services.parsers.base import BaseParser

class TextParser(BaseParser):
    """
    Parser for plain text, email dumps, or log files (.txt, .log, .eml, .json).
    Handles encoding fallbacks cleanly (UTF-8, Latin-1, CP1252).
    """
    def parse(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        encodings = ['utf-8', 'latin-1', 'cp1252']
        content = ""
        used_encoding = "unknown"

        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                used_encoding = enc
                break
            except Exception:
                continue

        line_count = len(content.splitlines())
        word_count = len(content.split())
        char_count = len(content)

        metadata = {
            "parser": "TextParser",
            "encoding": used_encoding,
            "line_count": str(line_count),
            "word_count": str(word_count),
            "character_count": str(char_count)
        }

        return content, metadata
