import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from storage.db_handler import fetch_all, create_table

create_table()

st.title("📊 MicroCredit Risk Dashboard")

# ------------------------------------------
# Load Data
# ------------------------------------------
df = fetch_all()

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# ------------------------------------------
# KPI METRICS
# ------------------------------------------
total = len(df)
repaid = len(df[df["outcome"] == "Repaid"])
defaulted = len(df[df["outcome"] == "Defaulted"])
default_rate = (defaulted / total) * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Borrowers", total)
col2.metric("Repaid", repaid)
col3.metric("Defaulted", defaulted)
col4.metric("Default Rate", f"{default_rate:.1f}%")

st.divider()
# ------------------------------------------
# DERIVED METRICS (FOR DASHBOARD)
# ------------------------------------------
high_risk = len(df[df["risk_level"] == "High Risk"])
high_risk_pct = (high_risk / total) * 100 if total > 0 else 0

most_common_loan = df["loan_type"].mode()[0]

# ------------------------------------------
# CHART 1: Repaid vs Defaulted
# ------------------------------------------
# CHARTS SECTION (FRAMED)
# ------------------------------------------
st.subheader("📊 Analytics Overview")

col1, col2 = st.columns(2)

# -------------------------------
# CARD 1: Loan Outcomes
# -------------------------------
with col1:
    with st.container():
        st.markdown("### 📊 Loan Outcomes")

        outcome_counts = df["outcome"].value_counts()

        fig1, ax1 = plt.subplots()
        outcome_counts.plot(kind="bar", ax=ax1)
        ax1.set_xlabel("")
        ax1.set_ylabel("Count")

        st.pyplot(fig1)

# -------------------------------
# CARD 2: Risk Distribution
# -------------------------------
with col2:
    with st.container():
        st.markdown("### 🥧 Risk Distribution")

        risk_counts = df["risk_level"].value_counts()

        fig2, ax2 = plt.subplots()
        risk_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax2)
        ax2.set_ylabel("")

        st.pyplot(fig2)
        col3, col4 = st.columns(2)

# -------------------------------
# CARD 3: Loan Type Distribution
# -------------------------------
with col3:
    with st.container():
        st.markdown("### 📈 Loan Types")

        loan_type_counts = df["loan_type"].value_counts()

        fig3, ax3 = plt.subplots()
        loan_type_counts.plot(kind="bar", ax=ax3)
        ax3.set_xlabel("")
        ax3.set_ylabel("Count")

        st.pyplot(fig3)

# -------------------------------
# CARD 4: Quick Summary
# -------------------------------
with col4:
    with st.container():
        st.markdown("### 🧠 Summary")

        # high_risk = len(df[df["risk_level"] == "High Risk"])
        st.metric("High Risk Borrowers", high_risk)
        st.metric("Default Rate", f"{default_rate:.1f}%")
        
st.divider()

# ------------------------------------------
# INSIGHTS SECTION
# ------------------------------------------
st.subheader("🧠 Key Insights")

high_risk = len(df[df["risk_level"] == "High Risk"])
high_risk_pct = (high_risk / total) * 100 if total > 0 else 0

st.info(f"🔎 {high_risk_pct:.1f}% of borrowers are classified as High Risk.")

most_common_loan = df["loan_type"].mode()[0]
st.info(f"📌 Most common loan type: {most_common_loan}")

if default_rate > 30:
    st.warning("⚠️ Default rate is high. Review lending strategy.")
else:
    st.success("✅ Default rate is within acceptable range.")