from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    credit_score = Column(Integer)
    annual_income = Column(Float)
    employment_years = Column(Integer)
    home_ownership = Column(String) # RENT, OWN, MORTGAGE
    
    loans = relationship("Loan", back_populates="borrower")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"))
    amount = Column(Float)
    term_months = Column(Integer)
    interest_rate = Column(Float)
    installment = Column(Float)
    grade = Column(String)
    issue_date = Column(DateTime)
    loan_status = Column(String) # Current, Default, Fully Paid
    
    borrower = relationship("Borrower", back_populates="loans")
    repayments = relationship("Repayment", back_populates="loan")
    features = relationship("LoanFeatures", uselist=False, back_populates="loan")


class Repayment(Base):
    __tablename__ = "repayments"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    payment_date = Column(DateTime)
    payment_amount = Column(Float)
    
    loan = relationship("Loan", back_populates="repayments")


class LoanFeatures(Base):
    __tablename__ = "loan_features"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    
    # Calculated Features
    repayment_velocity = Column(Float)
    credit_utilization_ratio = Column(Float)
    delinquency_freq = Column(Integer)
    debt_to_income_ratio = Column(Float)
    payment_consistency_score = Column(Float)
    
    # Target / Predictions
    default_probability = Column(Float)
    risk_segment = Column(String) # Low, Medium, High
    recommended_action = Column(String)
    
    loan = relationship("Loan", back_populates="features")
