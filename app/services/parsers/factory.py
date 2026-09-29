import os
from app.services.parsers.base import BaseParser
from app.services.parsers.text_parser import TextParser
from app.services.parsers.csv_parser import CSVParser
from app.services.parsers.pdf_parser import PDFParser

class ParserFactory:
    """
    Selects the appropriate evidence parser based on file extension and evidence type.
    """
    @staticmethod
    def get_parser(filename: str, evidence_type: str = "OTHER") -> BaseParser:
        ext = os.path.splitext(filename)[1].lower()
        type_upper = evidence_type.upper()
        
        if ext == '.pdf' or type_upper == 'PDF':
            return PDFParser()
        elif ext == '.csv':
            return CSVParser()
        elif ext in ['.txt', '.eml', '.log', '.json'] or type_upper in ['EMAIL', 'CHAT', 'OTHER', 'FINANCIAL_LOG', 'BROWSER_LOG', 'CALL_LOG']:
            return TextParser()
        else:
            # Default fallback parser
            return TextParser()
