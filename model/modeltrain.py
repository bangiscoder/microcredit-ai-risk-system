# ==========================================
# MicroCredit AI Risk System
# Model Training Script - Step 3
# ==========================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from utils.feature_engineering import apply_feature_engineering

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline



# ------------------------------------------
# 1. Load Cleaned Dataset
# ------------------------------------------

# Load dataset into pandas DataFrame
DATA_PATH = os.path.join("data", "processed", "cleaned_data.csv")
df = pd.read_csv(DATA_PATH)

print("Loaded cleaned dataset:", df.shape)

# Display basic info
print("Dataset Loaded Successfully")
print("Shape:", df.shape)
print(df.head())


# ------------------------------------------
# 2. Feature Engineering Applied in train.py
# ------------------------------------------
df = apply_feature_engineering(df)
print("\nFeature engineering completed.")
print("Final dataset shape:", df.shape)

print("After feature engineering:", df.shape)
print(df.columns)


# ------------------------------------------
# 3. Define Features and Target
# ------------------------------------------

TARGET = "Status"

# Drop target from features
X = df.drop(columns=[TARGET])
y = df[TARGET]

print("Features shape:", X.shape)
print("Target distribution:\n", y.value_counts())


# ------------------------------------------
# 4. Identify Column Types
# ------------------------------------------

# Numerical columns
num_cols = X.select_dtypes(include=["number"]).columns.tolist()

# Categorical columns
cat_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()

print("Numerical columns:", num_cols)
print("Categorical columns:", cat_cols)


# ------------------------------------------
# 5. Preprocessing Pipeline
# ------------------------------------------

# Numerical: scale
# Numeric pipeline
num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical pipeline
# Categorical: one-hot encode
cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


# Combine both
preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_transformer, num_cols),
        ("cat", cat_transformer, cat_cols)
    ]
)


# ------------------------------------------
# 6. Split Data
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)


# ------------------------------------------
# 7. Train Models
# ------------------------------------------

# Model 1: Logistic Regression
log_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

log_model.fit(X_train, y_train)

# Model 2: Random Forest
rf_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

rf_model.fit(X_train, y_train)


# ------------------------------------------
# 8. Evaluate Models
# ------------------------------------------

def evaluate(model, name):
    y_pred = model.predict(X_test)

    print(f"\n{name} Performance:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))


evaluate(log_model, "Logistic Regression")
evaluate(rf_model, "Random Forest")


# ------------------------------------------
# 9. Select Best Model
# ------------------------------------------

# Simple selection based on accuracy (you can refine later)
log_acc = accuracy_score(y_test, log_model.predict(X_test))
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))

best_model = rf_model if rf_acc > log_acc else log_model
best_name = "Random Forest" if rf_acc > log_acc else "Logistic Regression"

print(f"\nBest Model Selected: {best_name}")


# ------------------------------------------
# 10. Save Model
# ------------------------------------------

MODEL_PATH = os.path.join("model", "model.pkl")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(best_model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)