import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb
import os
import joblib

def train_models():
    print("Loading training data...")
    data_path = "CreditPathAI/data/processed/training_data.csv"
    if not os.path.exists(data_path):
        print("Training data not found!")
        return
        
    df = pd.read_csv(data_path)
    
    # Feature Selection
    features = [
        "repayment_velocity", "credit_utilization_ratio", 
        "delinquency_freq", "payment_consistency_score", 
        "amount", "interest_rate", "annual_income", "credit_score"
    ]
    target = "default_probability" # Currently 0/1 float
    
    # Drop rows with NaNs if any
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("CreditPathAI_Risk_Model")
    
    best_model = None
    best_auc = 0
    best_model_name = ""
    
    # 1. Baseline: Logistic Regression
    print("Training Logistic Regression...")
    with mlflow.start_run(run_name="Logistic_Regression"):
        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train, y_train)
        
        y_pred = lr.predict(X_test)
        y_prob = lr.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        print(f"LR AUC: {auc}")
        
        mlflow.log_metric("auc", auc)
        mlflow.sklearn.log_model(lr, "model")
        
        if auc > best_auc:
            best_auc = auc
            best_model = lr
            best_model_name = "Logistic_Regression"

    # 2. XGBoost
    print("Training XGBoost...")
    with mlflow.start_run(run_name="XGBoost"):
        xg_clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        xg_clf.fit(X_train, y_train)
        
        y_pred = xg_clf.predict(X_test)
        y_prob = xg_clf.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        print(f"XGB AUC: {auc}")
        
        mlflow.log_metric("auc", auc)
        # mlflow.xgboost.log_model(xg_clf, "model")
        
        if auc > best_auc:
            best_auc = auc
            best_model = xg_clf
            best_model_name = "XGBoost"
            
    # Save Best Model Locally
    print(f"Best Model: {best_model_name} with AUC: {best_auc}")
    os.makedirs("CreditPathAI/backend/app/artifacts", exist_ok=True)
    joblib.dump(best_model, "CreditPathAI/backend/app/artifacts/best_model.pkl")
    print("Model saved.")

if __name__ == "__main__":
    train_models()
