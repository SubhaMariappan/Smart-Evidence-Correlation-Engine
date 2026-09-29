import re

def normalize_email(email_str: str) -> str:
    """Normalizes email address to lowercase stripped format."""
    return email_str.strip().lower()

def normalize_phone(phone_str: str) -> str:
    """Normalizes phone number to standardized digit string."""
    cleaned = re.sub(r'[^\d+]', '', phone_str)
    if cleaned.startswith('+'):
        return '+' + re.sub(r'[^\d]', '', cleaned)
    digits = re.sub(r'[^\d]', '', cleaned)
    if len(digits) == 10:
        return digits
    return digits or phone_str.strip()

def normalize_ip(ip_str: str) -> str:
    """Normalizes IP address."""
    return ip_str.strip()

def normalize_person(name_str: str) -> str:
    """Normalizes person name to title case with collapsed whitespace."""
    cleaned = re.sub(r'\s+', ' ', name_str.strip())
    return cleaned.title()

def normalize_location(loc_str: str) -> str:
    """Normalizes location name to title case."""
    cleaned = re.sub(r'\s+', ' ', loc_str.strip())
    return cleaned.title()

def normalize_entity(raw_value: str, entity_type: str) -> str:
    """Master entity canonicalizer routing by entity_type."""
    t_upper = entity_type.upper()
    if t_upper == 'EMAIL':
        return normalize_email(raw_value)
    elif t_upper in ['PHONE', 'PHONE_NUMBER']:
        return normalize_phone(raw_value)
    elif t_upper == 'IP':
        return normalize_ip(raw_value)
    elif t_upper == 'PERSON':
        return normalize_person(raw_value)
    elif t_upper == 'LOCATION':
        return normalize_location(raw_value)
    else:
        return re.sub(r'\s+', ' ', raw_value.strip())
