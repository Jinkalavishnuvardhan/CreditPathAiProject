import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(num_samples=1000, output_dir="data/raw"):
    np.random.seed(42)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Borrowers
    borrower_ids = np.arange(1, num_samples + 1)
    
    borrowers = pd.DataFrame({
        "id": borrower_ids,
        "full_name": [f"Borrower_{i}" for i in borrower_ids],
        "credit_score": np.random.randint(580, 850, num_samples),
        "annual_income": np.random.lognormal(mean=11, sigma=0.5, size=num_samples),
        "employment_years": np.random.randint(0, 30, num_samples),
        "home_ownership": np.random.choice(["RENT", "OWN", "MORTGAGE"], num_samples, p=[0.4, 0.1, 0.5])
    })
    
    borrowers.to_csv(os.path.join(output_dir, "borrowers.csv"), index=False)
    print(f"Generated {num_samples} borrowers.")

    # 2. Loans
    loan_statuses = ["Current", "Fully Paid", "Charged Off", "Late (31-120 days)"]
    status_probs = [0.6, 0.25, 0.1, 0.05]
    
    loans = pd.DataFrame({
        "id": np.arange(1, num_samples + 1), # One loan per borrower for simplicity
        "borrower_id": borrower_ids,
        "amount": np.random.randint(1000, 40000, num_samples),
        "term_months": np.random.choice([36, 60], num_samples),
        "interest_rate": np.random.uniform(0.05, 0.25, num_samples),
        "grade": np.random.choice(["A", "B", "C", "D", "E"], num_samples),
        "issue_date": [datetime.today() - timedelta(days=np.random.randint(100, 1000)) for _ in range(num_samples)],
        "loan_status": np.random.choice(loan_statuses, num_samples, p=status_probs)
    })
    
    # Calculate approx installment
    r = loans["interest_rate"] / 12
    n = loans["term_months"]
    loans["installment"] = loans["amount"] * (r * (1 + r)**n) / ((1 + r)**n - 1)
    
    loans.to_csv(os.path.join(output_dir, "loans.csv"), index=False)
    print(f"Generated {num_samples} loans.")

    # 3. Repayments (Transaction History)
    repayment_rows = []
    
    for _, loan in loans.iterrows():
        # Generate varied repayment history based on status
        num_payments = np.random.randint(5, 20)
        start_date = loan["issue_date"]
        
        # Behavior modifier
        if loan["loan_status"] in ["Charged Off", "Late (31-120 days)"]:
            miss_prob = 0.3
        else:
            miss_prob = 0.05
            
        for i in range(1, num_payments + 1):
            if np.random.random() < miss_prob:
                continue # Missed payment
                
            pay_date = start_date + timedelta(days=30*i + np.random.randint(-5, 10))
            pay_amount = loan["installment"] * np.random.uniform(0.9, 1.1)            
            
            repayment_rows.append({
                "loan_id": loan["id"],
                "payment_date": pay_date,
                "payment_amount": round(pay_amount, 2)
            })
            
    repayments = pd.DataFrame(repayment_rows)
    repayments["id"] = range(1, len(repayments) + 1)
    repayments = repayments[["id", "loan_id", "payment_date", "payment_amount"]] # Reorder
    
    repayments.to_csv(os.path.join(output_dir, "repayments.csv"), index=False)
    print(f"Generated {len(repayments)} repayment records.")

if __name__ == "__main__":
    generate_synthetic_data(num_samples=2000, output_dir="CreditPathAI/data/raw")
