import re
from typing import List, Dict, Any

class RegexExtractor:
    """
    High-precision Regular Expression Entity Extractor for deterministic entities:
    - EMAIL
    - PHONE
    - IP
    - URL
    - ACCOUNT
    """
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
    PHONE_PATTERN = re.compile(r'\+?\d{1,3}[-.\s]?\d{5}[-.\s]?\d{5}|(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b')
    IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    URL_PATTERN = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+', re.IGNORECASE)
    ACCOUNT_PATTERN = re.compile(r'\b(ACCT-[A-Za-z0-9]+)\b|\b(?:account|acc|acct|a/c)[:\s#,=]*([a-zA-Z0-9_-]{6,24})\b', re.IGNORECASE)

    def extract(self, text: str) -> List[Dict[str, Any]]:
        results = []

        # 1. Emails
        for match in self.EMAIL_PATTERN.finditer(text):
            results.append({
                "entity_type": "EMAIL",
                "raw_value": match.group(0),
                "start_offset": match.start(),
                "end_offset": match.end(),
                "confidence": 1.0
            })

        # 2. Phone Numbers
        for match in self.PHONE_PATTERN.finditer(text):
            val = match.group(0)
            if not self.IP_PATTERN.match(val):
                results.append({
                    "entity_type": "PHONE",
                    "raw_value": val,
                    "start_offset": match.start(),
                    "end_offset": match.end(),
                    "confidence": 0.95
                })

        # 3. IP Addresses
        for match in self.IP_PATTERN.finditer(text):
            results.append({
                "entity_type": "IP",
                "raw_value": match.group(0),
                "start_offset": match.start(),
                "end_offset": match.end(),
                "confidence": 1.0
            })

        # 4. URLs
        for match in self.URL_PATTERN.finditer(text):
            results.append({
                "entity_type": "URL",
                "raw_value": match.group(0),
                "start_offset": match.start(),
                "end_offset": match.end(),
                "confidence": 1.0
            })

        # 5. Account Identifiers
        for match in self.ACCOUNT_PATTERN.finditer(text):
            if match.group(1):
                account_val = match.group(1)
                s_off, e_off = match.start(1), match.end(1)
            elif match.group(2):
                account_val = match.group(2)
                s_off, e_off = match.start(2), match.end(2)
            else:
                account_val = match.group(0)
                s_off, e_off = match.start(), match.end()

            results.append({
                "entity_type": "ACCOUNT",
                "raw_value": account_val,
                "start_offset": s_off,
                "end_offset": e_off,
                "confidence": 0.90
            })

        return results
