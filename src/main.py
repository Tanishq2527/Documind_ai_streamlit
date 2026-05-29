from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from PyPDF2 import PdfReader
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
import pytesseract
from PIL import Image


# import your existing logic
from src.utils import *
from src.nlp_utils import *
import re
import pytesseract

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📥 Request Model
class DocumentRequest(BaseModel):
    fileName: str
    fileType: str
    fileBase64: str


@app.post("/api/document-analyze")
def analyze_document(request: DocumentRequest, x_api_key: str = Header(...)):

    # 🔐 Check API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 📦 Decode Base64
    file_bytes = base64.b64decode(request.fileBase64)
    file_stream = BytesIO(file_bytes)

    # 📄 Read PDF (for now only PDF)
    file_type = request.fileType.lower()

    text = ""

# 📄 PDF
    if file_type == "pdf":
        reader = PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or ""

# 📝 DOCX
    elif file_type == "docx":
        doc = Document(file_stream)
        for para in doc.paragraphs:
            text += para.text + " "

# 🖼️ IMAGE (OCR)
    elif file_type in ["png", "jpg", "jpeg"]:
        image = Image.open(file_stream)
        text = pytesseract.image_to_string(image)

    else:
        return {"status": "error", "message": "Unsupported file type"}

    # 🧹 Clean text
    text = clean_text(text)

    # 🧠 NLP processing
    nlp = load_nlp()
    doc = nlp(text)

    persons = extract_persons(doc, is_valid_person)
    cleaned_persons = []

    

    cleaned_persons = []

    for p in persons:
        p = re.sub(r"\b(Company|Ltd|Inc|Corporation|Bank|Software)\b", "", p).strip()
        cleaned_persons.append(p)

    persons = list(set(cleaned_persons))


    dates = extract_dates(text)
    orgs = extract_orgs(text)
    money = extract_money(text)

    sentiment = analyze_sentiment(text)

    # 🧠 Summary
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    summary_sentences = summarizer(parser.document, 5)
    summary = " ".join(str(s) for s in summary_sentences)

    summary = " ".join(summary.split()[:100])

    # 📤 Response
   
    try:
        file_bytes = base64.b64decode(request.fileBase64)
    except Exception:
        return {"status": "error", "message": "Invalid Base64"}

    if len(file_bytes) == 0:
        return {"status": "error", "message": "Empty file"}
    
    return {
        "status": "success",
        "fileName": request.fileName,
        "summary": summary,
        "entities": {
            "names": persons,
            "dates": dates,
            "organizations": orgs,
            "amounts": money
        },
        "sentiment": sentiment
    }
