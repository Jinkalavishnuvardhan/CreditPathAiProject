import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Borrower, Loan, Repayment
import os
import sys

def ingest_data(data_dir="CreditPathAI/data/raw"):
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Load Borrowers
        print("Loading Borrowers...")
        borrowers_df = pd.read_csv(os.path.join(data_dir, "borrowers.csv"))
        borrowers = [Borrower(**row) for row in borrowers_df.to_dict(orient="records")]
        db.add_all(borrowers)
        db.commit()
        print(f"Loaded {len(borrowers)} borrowers.")
        
        # Load Loans
        print("Loading Loans...")
        loans_df = pd.read_csv(os.path.join(data_dir, "loans.csv"))
        # Convert date strings to datetime objects
        loans_df["issue_date"] = pd.to_datetime(loans_df["issue_date"])
        loans = [Loan(**row) for row in loans_df.to_dict(orient="records")]
        db.add_all(loans)
        db.commit()
        print(f"Loaded {len(loans)} loans.")
        
        # Load Repayments
        print("Loading Repayments...")
        repayments_df = pd.read_csv(os.path.join(data_dir, "repayments.csv"))
        repayments_df["payment_date"] = pd.to_datetime(repayments_df["payment_date"])
        
        # Process in chunks if too large
        chunk_size = 1000
        total_repayments = 0
        for i in range(0, len(repayments_df), chunk_size):
            chunk = repayments_df.iloc[i:i+chunk_size]
            repayments = [Repayment(**row) for row in chunk.to_dict(orient="records")]
            db.add_all(repayments)
            db.commit()
            total_repayments += len(chunk)
            
        print(f"Loaded {total_repayments} repayments.")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Adjust path if running from root
    base_path = "C:/Users/saikrishna/Downloads/Desktop/infosys_project"
    data_path = os.path.join(base_path, "CreditPathAI/data/raw")
    
    # Enable running module directly
    sys.path.append(os.path.join(base_path, "CreditPathAI/backend/app"))
    
    ingest_data(data_dir=data_path)
