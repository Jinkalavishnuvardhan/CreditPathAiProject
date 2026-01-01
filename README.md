# CreditPathAI

**Automating and Optimizing the Loan Recovery Lifecycle Using Machine Learning**

## Project Overview
CreditPathAI is an end-to-end AI system designed to predict borrower default risk, model repayment behavior, and recommend personalized loan recovery actions. It uses open-source technologies to provide a cost-effective, scalable, and interpretable solution for financial institutions.

## Features
- **Data Ingestion**: Automated pipeline to load and validate loan data into SQLite.
- **Feature Engineering**: Calculation of advanced metrics like Repayment Velocity and Payment Consistency.
- **Machine Learning**: 
  - predictive models (Logistic Regression, XGBoost) for default risk.
  - Experiment tracking via MLflow.
- **Risk Segmentation**: Classification of borrowers into Low, Medium, and High risk categories.
- **Action Recommendations**: Rule-based engine suggesting recovery strategies (e.g., SMS nudges vs. Legal action).
- **Interactive Dashboard**: React-based UI (CDN mode) for visualizing portfolio risk and analyzing individual borrowers.

## Technology Stack
- **Languages**: Python 3.9+, JavaScript (ES6+)
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Machine Learning**: scikit-learn, XGBoost, pandas, numpy, MLflow
- **Frontend**: React.js (via CDN), Plotly.js, TailwindCSS
- **Database**: SQLite3
- **Containerization**: Docker (optional)

## Installation & Running Locally

### Prerequisites
- Python 3.8+ installed.

### Quick Start (Windows)
1. Double-click `run_locally.bat`.
   - This script installs dependencies, starts the backend server, and opens the frontend in your browser.

### Manual Setup
1. **Install Dependencies**:
   ```bash
   pip install -r CreditPathAI/requirements.txt
   ```
2. **Run Backend**:
   ```bash
   cd CreditPathAI/backend/app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. **Run Frontend**:
   - Open `CreditPathAI/frontend/index.html` in your web browser.

## Project Structure
```
CreditPathAI/
├── backend/
│   ├── app/
│   │   ├── main.py          # API Entry point
│   │   ├── models.py        # Database Models
│   │   ├── train.py         # ML Training Script
│   │   ├── features.py      # Feature Engineering
│   │   └── recommendations.py # Recommendation Engine
│   └── tests/               # API Tests
├── data/                    # Raw and Processed Data
├── frontend/                # React Frontend (CDN)
├── docker/                  # Dockerfiles
├── requirements.txt         # Python Dependencies
└── README.md                # This file
```

## Usage
- **Risk Assessment Tab**: Enter borrower financial details to get a real-time risk score and recommendation.
- **Portfolio Dashboard Tab**: View aggregate risk distribution across the loan portfolio.
