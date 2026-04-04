import streamlit as st
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from utils import *
from src.nlp_utils import *
import nltk

@st.cache_resource
def load_model():
    return load_nlp()

nlp = load_model()

nltk.download('punkt')
nltk.download('punkt_tab')

st.set_page_config(page_title="DocuMind AI", layout="centered")

st.title("📄 DocuMind AI")
st.markdown("### Intelligent Document Analysis System")
st.markdown("---")

uploaded_file = st.file_uploader(
    "📤 Upload a PDF file",
    type=["pdf"],
    key="pdf_main"
)


if uploaded_file is not None:
    tabs = st.tabs(["📄 Text", "🧠 Summary", "🔍 Entities", "😊 Sentiment"])

    # Read PDF
    pdf_reader = PdfReader(uploaded_file)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    text = clean_text(text)

    with tabs[0]:
     st.subheader("📄 Extracted Text")
     st.text_area("Text", text, height=300)

    

    
   
        # ---------------- SUMMARY ----------------
    if text:
        with st.spinner("Generating summary..."):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()

            summary_sentences = summarizer(parser.document, 5)
            summary = " ".join(str(sentence) for sentence in summary_sentences)

            words = summary.split()
            summary = " ".join(words[:100])

        with tabs[1]:
            st.subheader("🧠 AI Summary")
            st.write(summary)


        # ---------------- ENTITIES ----------------
    if text:
        doc = nlp(text)

        persons = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if is_valid_person(ent.text):
                    persons.append(ent.text)

        money = extract_money(text)
        orgs = extract_orgs(text)
        orgs = [org for org in orgs if len(org.split()) >= 2]
        dates = extract_dates(text)

        persons = list(set(persons))
        dates = list(set(dates))
        orgs = list(set(orgs))
        money = list(set(money))

        with tabs[2]:
            st.subheader("🔍 Extracted Entities")

            col1, col2 = st.columns(2)

            with col1:
                st.write("👤 Names")
                st.write(persons if persons else "None")

                st.write("📅 Dates")
                st.write(dates if dates else "None")

            with col2:
                st.write("🏢 Organizations")
                st.write(orgs if orgs else "None")

                st.write("💰 Money")
                st.write(money if money else "None")

        # ---------------- SENTIMENT ----------------
    if text:
        with st.spinner("Analyzing sentiment..."):
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            if polarity > 0:
                sentiment = "Positive 😊"
            elif polarity < 0:
                sentiment = "Negative 😞"
            else:
                sentiment = "Neutral 😐"

        with tabs[3]:
            st.subheader("😊 Sentiment Analysis")
            st.write(f"### {sentiment}")