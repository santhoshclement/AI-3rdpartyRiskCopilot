from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI(title="AI Third-Party Risk API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.get("/")
def root():
    return {
        "status": "healthy",
        "application": "AI Third-Party Risk Command Center"
    }

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):

    uploaded_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    return {
        "message": "Files uploaded successfully",
        "files": uploaded_files
    }

@app.post("/analyze-risk")
async def analyze_risk(vendor: dict):

    score = 0

    if vendor.get("businessCritical"):
        score += 20

    if vendor.get("pii"):
        score += 15

    if vendor.get("paymentData"):
        score += 25

    if vendor.get("systemAccess"):
        score += 20

    if vendor.get("cloudHosted"):
        score += 10

    rating = "Low"

    if score > 30:
        rating = "Medium"

    if score > 60:
        rating = "High"

    if score > 80:
        rating = "Critical"

    return {
        "risk_score": score,
        "risk_rating": rating
    }
