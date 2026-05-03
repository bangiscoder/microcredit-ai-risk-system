# ==========================================
# Prediction Module
# MicroCredit AI Risk System
# ==========================================

# ------------------------------------------
# 0. IMPORTS AND PATH SETUP
# ------------------------------------------

import sys
import os

# Add project root to Python path (fix import issues)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import pandas as pd

from utils.feature_engineering import apply_feature_engineering


# ------------------------------------------
# 1. LOAD TRAINED MODEL
# ------------------------------------------

MODEL_PATH = os.path.join("model", "model.pkl")

# Load the trained pipeline (preprocessing + model)
model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")


# ------------------------------------------
# 2. MAIN PREDICTION FUNCTION
# ------------------------------------------

def predict_loan_risk(user_input: dict):
    """
    Predict loan default risk based on user input.

    Parameters:
        user_input (dict): dictionary containing borrower details

    Returns:
        dict: prediction result with risk level and probability
    """

    # --------------------------------------
    # Step 1: Convert user input to DataFrame
    # --------------------------------------
    df = pd.DataFrame([user_input])

    # --------------------------------------
    # Step 2: Apply feature engineering
    # (FOIR, age conversion, etc.)
    # --------------------------------------
    df = apply_feature_engineering(df)

    # --------------------------------------
    # Step 3: Handle missing values
    # --------------------------------------

    # Fill numeric columns with 0
    for col in df.select_dtypes(include=["number"]).columns:
        df[col] = df[col].fillna(0)

    # Fill categorical columns with "Unknown"
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].fillna("Unknown").astype(str)

    # --------------------------------------
    # Step 4: Align columns with training data
    # --------------------------------------

    # Get columns used during training
    expected_columns = model.feature_names_in_

    # Add missing columns (if any)
    # Get column types from training
    num_cols = model.named_steps['preprocessor'].transformers_[0][2]
    cat_cols = model.named_steps['preprocessor'].transformers_[1][2]

    for col in expected_columns:
        if col not in df.columns:
            if col in num_cols:
                df[col] = 0
            else:
                df[col] = "Unknown"
        # for col in expected_columns:
        #     if col not in df.columns:
        #         df[col] = 0

    # Ensure correct column order
    df = df[expected_columns]

    # --------------------------------------
    # Step 5: Make prediction
    # --------------------------------------

    # Predict class (0 = No Default, 1 = Default)
    prediction = model.predict(df)[0]

    # Predict probability of default
    probability = model.predict_proba(df)[0][1]

    # --------------------------------------
    # Step 6: Map to Risk Level
    # --------------------------------------

    if probability < 0.3:
        risk_level = "Low Risk"
    elif probability < 0.7:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # --------------------------------------
    # Step 7: Return Results
    # --------------------------------------

    return {
        "prediction": int(prediction),
        "probability": float(probability),
        "risk_level": risk_level
    }


# ------------------------------------------
# 3. TEST BLOCK (RUN FILE DIRECTLY)
# ------------------------------------------

if __name__ == "__main__":
    # Example test input
    # sample_input = {
    #     "loan_type": "type1",
    #     "loan_purpose": "p1",
    #     "business_or_commercial": "nob/c",
    #     "loan_amount": 200000,
    #     "rate_of_interest": 5.0,
    #     "term": 360,
    #     "employment_type": "salary",
    #     "loan_history_count": 1,
    #     "customer_reliability_score": 0.7,
    #     "income": 50000,
    #     "credit_type": "EXP",
    #     "Credit_Score": 700,
    #     "co-applicant_credit_type": "EXP",
    #     "age": 34
    # }

    sample_input = {
        "loan_type": "type1",
        "loan_purpose": "p1",
        "business_or_commercial": "nob/c",
        "loan_amount": 800000,
        "rate_of_interest": 10.0,
        "term": 60,
        "employment_type": "unknown",
        "loan_history_count": 0,
        "customer_reliability_score": 0.2,
        "income": 20000,
        "credit_type": "EXP",
        "Credit_Score": 400,
        "co-applicant_credit_type": "EXP",
        "age": 25
    }

    # Run prediction
    result = predict_loan_risk(sample_input)

    print("\nPrediction Result:")
    print(result)

    if not os.path.exists("model/model.pkl"):
        from model.modeltrain import train_model
        train_model()