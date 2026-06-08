from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="AI Third-Party Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VendorAssessment(BaseModel):
    vendorName: str
    businessCritical: bool
    pii: bool
    paymentData: bool
    systemAccess: bool
    cloudHosted: bool

@app.get("/")
def health():
    return {
        "status": "healthy",
        "application": "AI Third-Party Risk Command Center"
    }

@app.post("/analyze-risk")
def analyze_risk(data: VendorAssessment):

    score = 0

    if data.businessCritical:
        score += 20

    if data.pii:
        score += 15

    if data.paymentData:
        score += 25

    if data.systemAccess:
        score += 20

    if data.cloudHosted:
        score += 10

    if score <= 30:
        rating = "Low"
    elif score <= 60:
        rating = "Medium"
    elif score <= 80:
        rating = "High"
    else:
        rating = "Critical"

    return {
        "vendor": data.vendorName,
        "risk_score": score,
        "risk_rating": rating,
        "recommendation": "Review vendor controls, MFA, encryption, incident response and compliance evidence."
    }
