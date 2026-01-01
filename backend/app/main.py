from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os
from database import SessionLocal, get_db
from models import Borrower, Loan
from sqlalchemy.orm import Session
from sqlalchemy import func
from recommendations import RecommendationEngine

app = FastAPI(title="CreditPathAI API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "../../frontend")

if os.path.exists(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_dir}")

# Load Model
MODEL_PATH = "artifacts/best_model.pkl" 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FULL_PATH = os.path.join(BASE_DIR, MODEL_PATH)

try:
    model = joblib.load(MODEL_FULL_PATH)
    print(f"Model loaded from {MODEL_FULL_PATH}")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

rec_engine = RecommendationEngine()

class PredictionRequest(BaseModel):
    repayment_velocity: float
    credit_utilization_ratio: float
    delinquency_freq: int
    payment_consistency_score: float
    amount: float
    interest_rate: float
    annual_income: float
    credit_score: float

class RecommendationRequest(BaseModel):
    default_probability: float

from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url="/app/index.html")

@app.post("/predict")
def predict_risk(request: PredictionRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    data = pd.DataFrame([request.dict()])
    
    features = [
        "repayment_velocity", "credit_utilization_ratio", 
        "delinquency_freq", "payment_consistency_score", 
        "amount", "interest_rate", "annual_income", "credit_score"
    ]
    
    try:
        X = data[features]
        prob = model.predict_proba(X)[0][1] 
        rec = rec_engine.get_recommendation(prob)
        return rec
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_action(request: RecommendationRequest):
    return rec_engine.get_recommendation(request.default_probability)

@app.get("/loans/{loan_id}")
def get_loan_details(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {
        "id": loan.id,
        "amount": loan.amount,
        "status": loan.loan_status,
        "borrower": loan.borrower.full_name
    }

@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_loans = db.query(Loan).count()
    total_volume = db.query(Loan).with_entities(func.sum(Loan.amount)).scalar() or 0.0
    status_counts = db.query(Loan.loan_status, func.count(Loan.loan_status)).group_by(Loan.loan_status).all()
    status_dist = {s: c for s, c in status_counts}
    
    return {
        "total_loans": total_loans,
        "total_volume": total_volume,
        "status_distribution": status_dist
    }

@app.get("/borrowers")
def get_borrowers(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    try:
        loans = db.query(Loan).join(Borrower).offset(skip).limit(limit).all()
        results = []
        for loan in loans:
            results.append({
                "id": int(loan.borrower.id),
                "name": str(loan.borrower.full_name),
                "loan_amount": float(loan.amount) if loan.amount is not None else 0.0,
                "status": str(loan.loan_status),
                "credit_score": int(loan.borrower.credit_score) if loan.borrower.credit_score is not None else 0,
                "risk_segment": "Calculated on-demand"
            })
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Changed default port to 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)
