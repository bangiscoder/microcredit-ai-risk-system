# ================================
# MicroCredit AI Risk System
# Model Training Script - Step 1
# ================================

# Import required libraries
import sys
import pandas as pd
import numpy as np
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --------------------------------
# 1. Load Dataset
# --------------------------------

# Define dataset path
DATA_PATH = os.path.join("data", "raw", "loan_data.csv")

# Load dataset into pandas DataFrame
df = pd.read_csv(DATA_PATH)

# Display basic info
print("Dataset Loaded Successfully")
print("Shape:", df.shape)
print(df.head())


# --------------------------------
# 2. Drop Fully Empty Columns
# --------------------------------
# These columns have no data at all

df = df.dropna(axis=1, how='all')

print("\nAfter dropping empty columns:")
print(df.shape)


# --------------------------------
# 3. Drop Unwanted Columns
# --------------------------------
# Based on your system design

columns_to_drop = [
    "ID",
    "year",
    "Gender",
    "Region",
    "total_units",
    "Interest_rate_spread",
    "Upfront_charges",
    "submission_of_application",
    "Credit_Worthiness",
    "Credit_Score",
    "Credit_Type",
    "Co-Applicant_Credit_Type",
    "Reliability_Score"
]

# Drop only if they exist (safe approach)
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

print("\nAfter dropping unnecessary columns:")
print(df.shape)


# --------------------------------
# 4. Keep Only Relevant Columns
# --------------------------------
# Final feature list (your refined schema)

selected_columns = [
    "loan_type",
    "loan_purpose",
    "business_or_commercial",
    "loan_amount",
    "rate_of_interest",
    "term",
    "employment_type",
    "loan_history_count",
    "income",
    "age",
    "Status"
]

# Keep only columns that exist in dataset
df = df[[col for col in selected_columns if col in df.columns]]

print("\nFinal selected columns:")
print(df.columns)
print("Shape:", df.shape)

# ==========================================
# DATA VALUE CLEANING (MAKE VALUES READABLE)
# ==========================================

# ------------------------------------------
# 1. Loan Type (type1 → meaningful labels)
# ------------------------------------------
df["loan_type"] = df["loan_type"].map({
    "type1": "Personal Loan",
    "type2": "Business Loan",
    "type3": "Mortgage Loan"
})

# ------------------------------------------
# 2. Loan Purpose (p1 → readable purpose)
# ------------------------------------------
df["loan_purpose"] = df["loan_purpose"].map({
    "p1": "Home Purchase",
    "p2": "Education",
    "p3": "Business Expansion",
    "p4": "Other"
})

# ------------------------------------------
# 3. Loan Category (nob/c → readable form)
# ------------------------------------------
df["business_or_commercial"] = df["business_or_commercial"].map({
    "nob/c": "Personal",
    "b/c": "Business"
})

# ------------------------------------------
# 4. Handle Missing Values After Mapping
# ------------------------------------------
# Sometimes mapping may produce NaN if unexpected values exist

df["loan_type"] = df["loan_type"].fillna("Unknown")
df["loan_purpose"] = df["loan_purpose"].fillna("Other")
df["business_or_commercial"] = df["business_or_commercial"].fillna("Unknown")


# --------------------------------
# 5. Handle Missing Values (Basic)
# --------------------------------

# Fill numerical columns with median
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill categorical columns with mode
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\nMissing values handled.")


# --------------------------------
# 6. Save Cleaned Dataset
# --------------------------------

PROCESSED_PATH = os.path.join("data", "processed", "cleaned_data.csv")

# Create folder if it doesn't exist
os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

df.to_csv(PROCESSED_PATH, index=False)

print("\nCleaned dataset saved successfully.")

# ================================
# Additional Feature Engineering Steps
# ================================