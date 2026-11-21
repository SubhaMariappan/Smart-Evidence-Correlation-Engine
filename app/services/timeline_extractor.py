import re
from datetime import datetime, timezone
from typing import List, Dict, Any

DATE_PATTERNS = [
    # ISO 8601 / standard forensic log timestamps: 2026-09-15 08:32:10 or 2026-09-15T08:32:10Z
    r'\b(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)\b',
    # Date with slashes: 2026/09/15 08:32:10
    r'\b(\d{4}/\d{2}/\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?)\b',
    # Standalone ISO date: 2026-09-15
    r'\b(\d{4}-\d{2}-\d{2})\b',
    # DD/MM/YYYY or MM/DD/YYYY
    r'\b(\d{2}/\d{2}/\d{4}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?)\b'
]

def parse_flexible_datetime(dt_str: str) -> datetime | None:
    dt_str = dt_str.replace("Z", "+00:00").replace("/", "-").strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y",
        "%m-%d-%Y"
    ]
    # Strip any trailing tz for simple parsing if needed
    clean_dt = re.sub(r'[+-]\d{2}:?\d{2}$', '', dt_str)
    for fmt in formats:
        try:
            parsed = datetime.strptime(clean_dt, fmt)
            return parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None

def extract_timeline_events(text: str, max_events: int = 50) -> List[Dict[str, Any]]:
    """
    Scans document text for chronological timestamp indicators and extracts surrounding contextual lines.
    """
    if not text:
        return []

    events = []
    seen_timestamps = set()

    lines = text.splitlines()
    for line in lines:
        line_strip = line.strip()
        if not line_strip or len(line_strip) < 8:
            continue

        for pat in DATE_PATTERNS:
            match = re.search(pat, line_strip)
            if match:
                dt_str = match.group(1)
                parsed_dt = parse_flexible_datetime(dt_str)
                if parsed_dt:
                    ts_key = (parsed_dt.isoformat(), line_strip[:40])
                    if ts_key in seen_timestamps:
                        break
                    seen_timestamps.add(ts_key)

                    # Extract snippet
                    snippet = line_strip
                    if len(snippet) > 200:
                        snippet = snippet[:197] + "..."

                    # Determine an informative title
                    title = f"Document Activity [{dt_str}]"
                    if "login" in snippet.lower() or "auth" in snippet.lower():
                        title = f"Authentication Event [{dt_str}]"
                        evt_type = "ACCESS"
                    elif "transfer" in snippet.lower() or "payment" in snippet.lower() or "$" in snippet:
                        title = f"Financial Transaction [{dt_str}]"
                        evt_type = "TRANSACTION"
                    elif "email" in snippet.lower() or "sent" in snippet.lower() or "received" in snippet.lower() or "chat" in snippet.lower():
                        title = f"Communication Event [{dt_str}]"
                        evt_type = "COMMUNICATION"
                    else:
                        evt_type = "FORENSIC_TIMESTAMP"

                    events.append({
                        "event_timestamp": parsed_dt,
                        "title": title,
                        "description": snippet,
                        "event_type": evt_type
                    })
                    break  # One event per line is sufficient
        if len(events) >= max_events:
            break

    return events
