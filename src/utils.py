import re

def clean_text(text):

    # normalize spacing
    text = text.replace("\n", " ")

    # add space after colon
    text = re.sub(r":", ": ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove weird characters
    text = re.sub(r"[^a-zA-Z0-9.,₹$/:\- ]", "", text)

    return text.strip()

def is_valid_person(name):
    import re

    # 🔥 Remove unwanted words from end
    name = re.sub(r"\b(Company|Ltd|Inc|Corporation|Bank|Software)\b", "", name).strip()

    words = name.split()

    # must be 2–3 words
    if len(words) < 2 or len(words) > 3:
        return False

    # all words must start with capital
    if not all(word[0].isupper() for word in words):
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