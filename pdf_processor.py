# pdf_processor.py

import fitz  # PyMuPDF
import openai

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sammanfatta enligt svenska riktlinjer för kolorektal cancer."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message["content"]

def analyze_patient_data(data_dict):
    # Här kan du matcha mot riktlinjer i framtiden.
    return f"Patient med {data_dict['tnm']} och {data_dict['histopatologi']}, rekommenderas bedömning enligt MDT."
