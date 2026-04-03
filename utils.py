import re

def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,₹$/\- ]', '', text)
    return text.strip()

def is_valid_person(name):
    words = name.split()
    if len(words) < 2 or len(words) > 3:
        return False
    if not all(word[0].isupper() for word in words):
        return False
    if any(char.isdigit() for char in name):
        return False
    return True

def extract_money(text):
    pattern = r"(₹\s?\d+(?:,\d+)*(?:\.\d+)?|\$\s?\d+(?:,\d+)*(?:\.\d+)?)"
    return re.findall(pattern, text)

def extract_orgs(text):
    pattern = r"\b[A-Z][a-zA-Z&]+(?:\s[A-Z][a-zA-Z&]+){0,2}\s(?:Software|Company|Corporation|Inc|Ltd|Bank|College|University)\b"
    return list(set(re.findall(pattern, text)))

def extract_dates(text):
    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\b\d{1,2}-\d{1,2}-\d{4}\b",
        r"\b\d{1,2}/\d{4}\b",
        r"\b\d{1,2}-\d{4}\b",
        r"\b(19\d{2}|20\d{2})\b"
    ]
    dates = []
    for p in patterns:
        for m in re.finditer(p, text):
            dates.append(m.group())
    return list(set(dates))