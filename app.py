from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf_processor import extract_text_from_pdf, summarize_text, analyze_patient_data
import os

app = Flask(__name__)
CORS(app)  # gör att frontend (Compose-appen) kan kommunicera med backend

# Lägg din PDF i denna mapp
PDF_PATH = "uploads/riktlinjer.pdf"

# Sammanfatta PDF:en en gång när servern startar
if os.path.exists(PDF_PATH):
    print("🔍 Läser PDF...")
    riktlinjetext = extract_text_from_pdf(PDF_PATH)
    sammanfattning = summarize_text(riktlinjetext)
    print("✅ Riktlinjer sammanfattade.")
else:
    sammanfattning = ""
    print("⚠️ Ingen PDF hittades – sammanfattning inte tillgänglig.")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json  # patientdata som skickas från Compose
    if not sammanfattning:
        return jsonify({"error": "Ingen riktlinje-sammanfattning tillgänglig."}), 400

    # Format patientdata som text
    patient_data = "\n".join([f"{key}: {value}" for key, value in data.items()])

    print("🧠 Skickar patientdata till AI...")
    bedomning = analyze_patient_data(patient_data, sammanfattning)

    return jsonify({
        "bedomning": bedomning
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

