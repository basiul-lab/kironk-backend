from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pdf_processor import extract_text_from_pdf, summarize_text, analyze_patient_data

app = Flask(__name__)
CORS(app)

PDF_PATH = "uploads/riktlinje.pdf"
PDF_TEXT = ""

# Skapas automatiskt om saknas
os.makedirs("uploads", exist_ok=True)

@app.before_first_request
def preload_pdf():
    global PDF_TEXT
    if os.path.exists(PDF_PATH):
        print("📄 Läser in PDF...")
        PDF_TEXT = extract_text_from_pdf(PDF_PATH)
        print("✅ PDF inläst!")
    else:
        print("⚠️ Ingen PDF hittades vid uppstart.")

@app.route("/admin-upload", methods=["POST"])
def upload_pdf():
    global PDF_TEXT
    file = request.files.get("file")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Ingen giltig PDF laddad"}), 400

    file.save(PDF_PATH)
    PDF_TEXT = extract_text_from_pdf(PDF_PATH)
    return jsonify({"message": "✅ PDF uppladdad och inläst"})

@app.route("/generate", methods=["POST"])
def generate_mdt():
    global PDF_TEXT
    data = request.get_json()
    if not data:
        return jsonify({"error": "Inga data mottagna"}), 400

    if not PDF_TEXT:
        return jsonify({"error": "Riktlinje-PDF saknas. Ladda upp via /admin-upload"}), 500

    try:
        result = analyze_patient_data(data, PDF_TEXT)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
