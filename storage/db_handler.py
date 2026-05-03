import sqlite3
from datetime import datetime
import pandas as pd

DB_PATH = "storage/database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_type TEXT,
            nin TEXT,
            bvn TEXT,
            name TEXT,
            gender TEXT,
            state TEXT,
            loan_purpose TEXT,
            business_or_commercial TEXT,
            loan_amount REAL,
            rate_of_interest REAL,
            term INTEGER,
            income REAL,
            age INTEGER,
            employment_type TEXT,
            loan_history_count INTEGER,
            prediction INTEGER,
            probability REAL,
            risk_level TEXT,
            outcome TEXT,
            created_at TEXT
        )
    """ 
    )

    conn.commit()
    conn.close()


def insert_application(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO applications (
        loan_type,
        nin,
        bvn,
        name,
        gender,
        state,
        loan_purpose,
        business_or_commercial,
        loan_amount,
        rate_of_interest,
        term,
        income,
        age,
        employment_type,
        loan_history_count,
        prediction,
        probability,
        risk_level,
        outcome,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (*data, None, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def fetch_all():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM applications", conn)
    conn.close()
    return df


def update_outcome(app_id, outcome):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET outcome=? WHERE id=?",
        (outcome, app_id)
    )

    conn.commit()
    conn.close()