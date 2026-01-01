from fastapi.testclient import TestClient
import sys
import os

# Add app to path
sys.path.append(os.path.join(os.getcwd(), "CreditPathAI/backend/app"))

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CreditPathAI API"}

def test_predict_endpoint():
    # Sample data
    payload = {
        "repayment_velocity": 0.8,
        "credit_utilization_ratio": 0.3,
        "delinquency_freq": 0,
        "payment_consistency_score": 500.0,
        "amount": 10000.0,
        "interest_rate": 0.1,
        "annual_income": 60000.0,
        "credit_score": 750.0
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_segment" in data
    assert "recommended_actions" in data
    print(f"Prediction Response: {data}")

def test_recommend_endpoint():
    payload = {"default_probability": 0.7}
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_segment"] == "High Risk"

if __name__ == "__main__":
    try:
        test_read_root()
        test_predict_endpoint()
        test_recommend_endpoint()
        print("All API tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
