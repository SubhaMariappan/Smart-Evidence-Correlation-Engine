import csv
from typing import Tuple, Dict, Any
from app.services.parsers.base import BaseParser

class CSVParser(BaseParser):
    """
    Parser for structured CSV evidence (bank statements, call logs, transaction exports).
    Serializes CSV rows into readable text and extracts structural metadata.
    """
    def parse(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        rows_text = []
        headers = []
        row_count = 0
        used_encoding = "unknown"

        encodings = ['utf-8', 'latin-1', 'cp1252']

        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    reader = csv.reader(f)
                    all_rows = list(reader)
                    if all_rows:
                        headers = all_rows[0]
                        row_count = len(all_rows) - 1
                        for idx, row in enumerate(all_rows):
                            rows_text.append(f"Row {idx}: " + ", ".join(row))
                    used_encoding = enc
                    break
            except Exception:
                continue

        content = "\n".join(rows_text)

        metadata = {
            "parser": "CSVParser",
            "encoding": used_encoding,
            "headers": ", ".join(headers) if headers else "",
            "header_count": str(len(headers)),
            "row_count": str(row_count),
            "total_lines": str(len(rows_text))
        }

        return content, metadata
