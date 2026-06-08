from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pypdf import PdfReader
import os
import shutil

app = FastAPI(title="AI Third-Party Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def extract_pdf_text(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:15000]

def extract_txt_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()[:15000]

@app.get("/")
def health():
    return {
        "status": "healthy",
        "application": "AI Third-Party Risk Command Center"
    }

@app.post("/ai-assess")
async def ai_assess(
    vendor_name: str = Form(...),
    service: str = Form(...),
    country: str = Form(...),
    business_critical: str = Form(...),
    pii: str = Form(...),
    payment_data: str = Form(...),
    system_access: str = Form(...),
    cloud_hosted: str = Form(...),
    files: list[UploadFile] = File(...)
):
    combined_text = ""

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.lower().endswith(".pdf"):
            combined_text += extract_pdf_text(file_path)
        elif file.filename.lower().endswith(".txt"):
            combined_text += extract_txt_text(file_path)

    prompt = f"""
You are an AI Third-Party Cyber Risk Assessment Assistant.

Analyze the vendor profile and uploaded document evidence.

Vendor:
- Name: {vendor_name}
- Service: {service}
- Country: {country}
- Business Critical: {business_critical}
- Handles PII: {pii}
- Handles Payment Data: {payment_data}
- Requires System Access: {system_access}
- Cloud Hosted: {cloud_hosted}

Document Evidence:
{combined_text}

Return a professional third-party risk report with:

1. Executive Summary
2. Overall Risk Rating: Low / Medium / High / Critical
3. Key Security Findings
4. Missing Controls
5. Evidence Found
6. Recommended Vendor Questions
7. Risk Treatment Recommendation
8. Approval Decision
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "vendor": vendor_name,
        "ai_report": response.text
    }
