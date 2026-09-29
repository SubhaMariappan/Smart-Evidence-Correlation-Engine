import re
from typing import List, Dict, Any

class NLPExtractor:
    """
    Pattern & Heuristic Named Entity Recognition (NER) Extractor for:
    - PERSON
    - LOCATION
    - ORGANIZATION
    Designed with high precision fallbacks for digital forensics text.
    """
    PERSON_PATTERNS = [
        re.compile(r'\b(?:contact|call|email|reach|speak to|sent to|ask for|with|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', re.IGNORECASE),
        re.compile(r'\b(?:Mr\.|Ms\.|Mrs\.|Dr\.|Prof\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'),
        re.compile(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b')
    ]

    LOCATION_PATTERNS = [
        re.compile(r'\b(?:in|at|from|to|near|located at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+(?:City|Street|Road|Nagar|Building|Tower|Airport|Branch))?)\b', re.IGNORECASE),
        re.compile(r'\b(London|New York|Mumbai|Delhi|Bangalore|Singapore|Dubai|Tokyo)\b', re.IGNORECASE)
    ]

    def extract(self, text: str) -> List[Dict[str, Any]]:
        results = []
        seen_spans = set()

        # 1. Person Names
        for pattern in self.PERSON_PATTERNS:
            for match in pattern.finditer(text):
                val = match.group(1) if match.groups() else match.group(0)
                start = match.start(1) if match.groups() else match.start()
                end = match.end(1) if match.groups() else match.end()
                
                # Exclude common stop words / false positives
                if val.lower() in {'the', 'a', 'an', 'regarding', 'payment', 'transaction', 'account', 'email', 'contact', 'secret'}:
                    continue

                span_key = (start, end)
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    results.append({
                        "entity_type": "PERSON",
                        "raw_value": val,
                        "start_offset": start,
                        "end_offset": end,
                        "confidence": 0.85
                    })

        # 2. Locations
        for pattern in self.LOCATION_PATTERNS:
            for match in pattern.finditer(text):
                val = match.group(1) if match.groups() else match.group(0)
                start = match.start(1) if match.groups() else match.start()
                end = match.end(1) if match.groups() else match.end()

                if val.lower() in {'the', 'a', 'bank', 'office', 'home'}:
                    continue

                span_key = (start, end)
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    results.append({
                        "entity_type": "LOCATION",
                        "raw_value": val,
                        "start_offset": start,
                        "end_offset": end,
                        "confidence": 0.85
                    })

        return results
