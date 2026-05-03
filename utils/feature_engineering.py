# ==========================================
# Feature Engineering Module
# MicroCredit AI Risk System
# ==========================================

import pandas as pd
import numpy as np


# ------------------------------------------
# 1. Convert Age Range to Numeric
# ------------------------------------------
def convert_age(age_value):
    """
    Converts age ranges like '25-34' to midpoint (e.g. 29.5)
    """
    try:
        if isinstance(age_value, str) and "-" in age_value:
            lower, upper = age_value.split("-")
            return (int(lower) + int(upper)) / 2
        else:
            return np.nan
    except:
        return np.nan


# ------------------------------------------
# 2. Create FOIR (Fixed Obligation to Income Ratio)
# ------------------------------------------
def calculate_foir(df):
    """
    FOIR = Monthly Loan Payment / Monthly Income
    Monthly Payment ≈ loan_amount / term
    """

    # Avoid division by zero
    df["income"] = df["income"].replace(0, np.nan)

    # Monthly payment approximation
    df["monthly_payment"] = df["loan_amount"] / df["term"]

    # FOIR calculation
    df["FOIR"] = df["monthly_payment"] / df["income"]

    # Replace NaN values with 0
    df["FOIR"] = df["FOIR"].fillna(0)

    return df


# ------------------------------------------
# 3. Create Employment Type (If Missing)
# ------------------------------------------
def create_employment_type(df):
    """
    Since dataset may not have employment_type,
    we simulate based on available data
    """

    if "employment_type" not in df.columns:
        df["employment_type"] = "Unknown"

    return df


# ------------------------------------------
# 4. Create Loan History Count
# ------------------------------------------
def create_loan_history(df):
    """
    Simulate loan history count
    """
    if "loan_history_count" not in df.columns:
        df["loan_history_count"] = np.random.randint(0, 5, size=len(df))

    return df


# ------------------------------------------
# 5. Create Customer Reliability Score
# ------------------------------------------
def create_reliability_score(df):
    """
    Simulate reliability score between 0 and 1
    """
    if "customer_reliability_score" not in df.columns:
        df["customer_reliability_score"] = np.random.uniform(0.3, 0.9, size=len(df))

    return df


# ------------------------------------------
# 6. Apply All Feature Engineering Steps
# ------------------------------------------
def apply_feature_engineering(df):
    """
    Main function to apply all transformations
    """

    # Convert age
    df["age"] = df["age"].apply(convert_age)

    # Fill missing age values
    df["age"] = df["age"].fillna(df["age"].median())

    # Create FOIR
    df = calculate_foir(df)

    # Add missing system features
    df = create_employment_type(df)
    df = create_loan_history(df)
    df = create_reliability_score(df)

    return df