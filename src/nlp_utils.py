import spacy
from textblob import TextBlob



spacy.cli.download("en_core_web_sm")

def load_nlp():
    return spacy.load("en_core_web_sm")


import spacy

def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

def extract_persons(doc, is_valid_person):
    persons = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if is_valid_person(ent.text):
                persons.append(ent.text)
    return list(set(persons))

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😞"
    else:
        return "Neutral 😐"