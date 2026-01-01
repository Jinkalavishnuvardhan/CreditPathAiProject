import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Loan, Repayment, LoanFeatures, Borrower
import sys
import os

def calculate_features():
    db = SessionLocal()
    print("Fetching data from DB...")
    
    # Load data into Pandas
    loans_query = db.query(Loan)
    loans_df = pd.read_sql(loans_query.statement, db.bind)
    
    repayments_query = db.query(Repayment)
    repayments_df = pd.read_sql(repayments_query.statement, db.bind)

    borrowers_query = db.query(Borrower)
    borrowers_df = pd.read_sql(borrowers_query.statement, db.bind)
    
    # Merge Borrower info into Loans
    loans_df = loans_df.merge(borrowers_df, left_on="borrower_id", right_on="id", suffixes=("", "_borrower"))
    
    print(f"Loaded {len(loans_df)} loans (with borrower info) and {len(repayments_df)} repayments.")
    
    feature_rows = []
    
    # Simple logic to map existing status to binary target
    # Default = 1 if Charged Off or Late, 0 otherwise
    # In real world, we'd predict probability, but for training we need labels
    def get_target(status):
        if status in ["Charged Off", "Late (31-120 days)"]:
            return 1
        return 0

    print("Calculating features...")
    for _, loan in loans_df.iterrows():
        loan_id = loan["id"]
        loan_repayments = repayments_df[repayments_df["loan_id"] == loan_id]
        
        # 1. Repayment Velocity: Amount paid / Expected amount by now
        # Simplified: Total paid / Loan Amount (Not exactly time-based but a proxy for progress)
        total_paid = loan_repayments["payment_amount"].sum() if not loan_repayments.empty else 0.0
        repayment_ratio = total_paid / loan["amount"] if loan["amount"] > 0 else 0
        
        # 2. Delinquency Frequency: Count of missed/late payments (Simulated logic from data gen)
        # In our gen script, we just skipped months. So let's count expected payments vs actual.
        # This is a bit complex to reverse engineer exactly without schedule, 
        # so we'll use a derived metric: (Months since issue) - (Count of payments)
        # valid mainly for active loans.
        months_since_issue = (pd.Timestamp.now() - pd.to_datetime(loan["issue_date"])).days / 30
        missed_payment_est = max(0, int(months_since_issue) - len(loan_repayments))
        
        # 3. Payment Consistency: Std Dev of payment amounts
        consistency = loan_repayments["payment_amount"].std() if len(loan_repayments) > 1 else 0.0
        if pd.isna(consistency): consistency = 0.0
        
        # 4. Debt to Income (Annual Input)
        # We need borrower info for this, let's skip or join. 
        # Actually models.py has borrower relationship.
        # For efficiency, we will fetch borrower income via join or new query. 
        # Let's do a join in SQL read above or just fetch separately. 
        # I'll update the initial query to join, or for now just use random consistency to prove pipeline.
        
        target = get_target(loan["loan_status"])
        
        feature_rows.append({
            "loan_id": loan_id,
            "repayment_velocity": round(repayment_ratio, 4),
            "credit_utilization_ratio": np.random.uniform(0.1, 0.9), # Mocked as external data
            "delinquency_freq": missed_payment_est,
            "debt_to_income_ratio": 0.0, # Placeholder
            "payment_consistency_score": round(consistency, 2),

            "default_probability": float(target), # Using target as proxy for 'truth' for now
            "risk_segment": "Unknown",
            "recommended_action": "None"
        })
        
    print("Saving features to DB...")
    # Bulk insert
    # First clear old features?
    db.query(LoanFeatures).delete()
    db.commit()
    
    features_df = pd.DataFrame(feature_rows)
    features_data = features_df.to_dict(orient="records")
    
    db.bulk_insert_mappings(LoanFeatures, features_data)
    db.commit()
    
    # Save training dataset
    final_df = loans_df.merge(features_df, left_on="id", right_on="loan_id")
    os.makedirs("CreditPathAI/data/processed", exist_ok=True)
    final_df.to_csv("CreditPathAI/data/processed/training_data.csv", index=False)
    print("Features saved and training data exported.")

if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), "CreditPathAI/backend/app"))
    calculate_features()
