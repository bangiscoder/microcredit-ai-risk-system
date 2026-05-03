import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from storage.db_handler import fetch_all, update_outcome
from storage.db_handler import create_table

create_table()

st.title("📋 Records")

df = fetch_all()

st.dataframe(df)

app_id = st.number_input("Application ID", min_value=1)
outcome = st.selectbox("Outcome", ["Repaid", "Defaulted"])

if st.button("Update"):
    update_outcome(app_id, outcome)
    st.success("Updated!")