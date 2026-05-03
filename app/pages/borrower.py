import sys
import os
MODEL_URL = "https://drive.google.com/uc?export=download&id=1mDMRd5Ghp3gMcVAYoY8o-YrbWKQ-zRPT"
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    r = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)

model = joblib.load(MODEL_PATH)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from model.predict import predict_loan_risk
from storage.db_handler import insert_application
from storage.db_handler import create_table

# Load remote model from Google Drive
import requests
import joblib
import os

# ------------------------------------------
# Initialize Session State Defaults
# ------------------------------------------
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "name": "",
        "age": 30,
        "gender": "Male",
        "state": "Bauchi",
        "nin": "",
        "bvn": "",
        "loan_amount": 100000,
        "income": 50000,
        "term": 360,
        "rate_of_interest": 5.0,
        "loan_history_count": 1,
        "employment_type": "Salary"
    }

create_table()

st.title("➕ Add Borrower")

# ------------------------------------------
# SECTION 1: PERSONAL DATA
# ------------------------------------------
st.subheader("👤 Borrower Personal Data")
st.caption("Basic identity information")

# --- Inputs (same as before) ---
name = st.text_input("Full Name", key="name")
age = st.number_input("Age", 18, 100, key="age")
gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
state = st.selectbox("State", ["Bauchi", "Kaduna", "Kano", "Lagos", "Abuja"], key="state")

nin = st.text_input("National Identification Number (NIN)", key="nin", max_chars=11)
bvn = st.text_input("Bank Verification Number (BVN)", key="bvn", max_chars=10)

st.divider()

# ------------------------------------------
# VALIDATION
# ------------------------------------------
def validate_ids(nin, bvn):
    errors = []

    # NIN validation
    if not nin.isdigit():
        errors.append("NIN must contain only numbers.")
    elif len(nin) != 11:
        errors.append("NIN must be exactly 11 digits.")

    # BVN validation
    if not bvn.isdigit():
        errors.append("BVN must contain only numbers.")
    elif len(bvn) != 10:
        errors.append("BVN must be exactly 10 digits.")

    return errors

if nin and (not nin.isdigit() or len(nin) > 11):
    st.warning("NIN must be numeric and max 11 digits")

if bvn and (not bvn.isdigit() or len(bvn) > 10):
    st.warning("BVN must be numeric and max 10 digits")

# ------------------------------------------
# SECTION 2: Loan Details
# ------------------------------------------

st.subheader("📄 Loan Details")

loan_type_display = st.selectbox(
    "Loan Type",
    ["Personal Loan", "Business Loan", "Mortgage Loan"]
)

loan_purpose_display = st.selectbox(
    "Loan Purpose",
    ["Home Purchase", "Education", "Business Expansion", "Other"]
)

business_type = st.selectbox(
    "Loan Category",
    ["Personal", "Business"]
)

# ------------------------------------------
# SECTION 3: FINANCIAL DATA
# ------------------------------------------
st.subheader("💰 Financial Information")
st.caption("Loan and income details")

loan_amount = st.number_input("Loan Amount", 1000, 1000000, key="loan_amount")
income = st.number_input("Income", 1000, 1000000, key="income")
term = st.number_input("Term", 1, 360, key="term")
rate_of_interest = st.number_input("Interest Rate (%)", 0.0, 30.0, key="rate_of_interest")


# ------------------------------------------
# SECTION 5: Behavioural Indicators
# # ------------------------------------------
st.subheader("📊 Behavioural Indicators")

loan_history_count = st.slider("Previous Loans", 0, 20, key="loan_history_count")
employment_type = st.selectbox("Employment Type", ["Salary", "Business", "Unemployed"], key="employment_type")


# ------------------------------------------
# Model Inforation Section
# # ------------------------------------------
# Example minimal input (you can expand later)
user_input = {
    "loan_type": "Personal Loan",
    "loan_purpose": "Home Purchase",
    "business_or_commercial": "Personal",
    "loan_amount": loan_amount,
    "rate_of_interest": 3.5,
    "term": term,
    "employment_type": "salary",
    "loan_history_count": 1,
    "income": income,
    "age": age
}

# ------------------------------------------
# Predict
# ------------------------------------------
if st.button("🔍 Predict Risk"):

    # -------------------------------
    # Validate Identity Fields
    # -------------------------------
    errors = []

    if not nin.isdigit():
        errors.append("BVN must contain only numbers.")
    elif len(bvn) != 10:
        errors.append("BVN must be exactly 10 digits.")

    if not nin.isdigit():
        errors.append("NIN must contain only numbers.")
    elif len(nin) != 11:
        errors.append("NIN must be exactly 11 digits.")

    # -------------------------------
    # Validate Required Fields
    # -------------------------------
    if not name:
        errors.append("Full Name is required.")

    if loan_amount <= 0:
        errors.append("Loan amount must be greater than zero.")

    if income <= 0:
        errors.append("Income must be greater than zero.")

    # -------------------------------
    # Stop if errors exist
    # -------------------------------
    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    # -------------------------------
    # Run Prediction (with spinner)
    # -------------------------------
    with st.spinner("Analyzing borrower risk..."):

        result = predict_loan_risk(user_input)

        # Save to session state
        st.session_state["result"] = result
        st.session_state["user_input"] = user_input


# ------------------------------------------
# Show Result
# ------------------------------------------
if "result" in st.session_state:

    result = st.session_state["result"]

    #  -------------------------------------------
    #  The follwing code displays the result in a nice format
    #  -------------------------------------------

    st.subheader("📊 Prediction Result")

    # Risk Level (visual)
    if result["risk_level"] == "Low Risk":
        st.success("✅ Low Risk - Loan can be approved")
    elif result["risk_level"] == "Medium Risk":
        st.warning("⚠️ Medium Risk - Review required")
    else:
        st.error("❌ High Risk - Not recommended")

    # Probability
    st.metric(
        label="Probability of Default",
        value=f"{result['probability']*100:.1f}%"
    )

    reasons = []

    if income < 30000:
        reasons.append("Low income")

    if loan_amount > income * 10:
        reasons.append("High loan burden")

    if reasons:
        st.info("🔎 Reason(s): " + ", ".join(reasons))
    else:
        st.info("🔎 Strong financial profile")

    # Decision
    decision = "Approve Loan" if result["prediction"] == 0 else "Reject Loan"

    st.write(f"**System Decision:** {decision}")

    if st.button("Save to Database"):
        insert_application((
            user_input["loan_type"],
            nin,
            bvn,
            name, 
            gender,
            state,
            user_input["loan_purpose"],
            user_input["business_or_commercial"],
            loan_amount,
            rate_of_interest,
            term,
            income,
            age,
            employment_type,
            loan_history_count,
            int(result["prediction"]),
            float(result["probability"]),
            result["risk_level"]
        ))

        st.success("✅ Record saved successfully!")

        # ------------------------------------------
        # Reset Form AFTER saving
        # ------------------------------------------
        for key in [
            "name", "age", "gender", "state",
            "nin", "bvn",
            "loan_amount", "income", "term",
            "rate_of_interest", "loan_history_count",
            "employment_type"
        ]:
            if key in st.session_state:
                del st.session_state[key]

        # Clear prediction result
        if "result" in st.session_state:
            del st.session_state["result"]

        if "user_input" in st.session_state:
            del st.session_state["user_input"]

    st.rerun()