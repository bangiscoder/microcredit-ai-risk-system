# 💰 MicroCredit AI Risk System (MARS)

An AI-powered decision support system designed to help microcredit institutions predict loan default risk and make data-driven lending decisions.

---

## 📌 Project Overview

Microcredit institutions in many communities rely on manual decision-making when issuing loans. This often leads to:

- High default rates  
- Bias towards known individuals  
- Exclusion of potentially reliable borrowers  

**MARS (MicroCredit AI Risk System)** addresses this by providing a machine learning-based system that predicts the likelihood of loan default before approval.

---

## 🎯 Problem Statement

Through my work with community-based organisations (CBOs) in Bauchi State, I observed that:

- Loan approvals depend heavily on:
  - Personal relationships  
  - Availability of civil servant guarantors  
- Many borrowers still default despite strict selection  
- Good borrowers are often excluded due to lack of connections  

As a result:

> ❌ Financial inclusion is reduced  
> ❌ Default rates remain high  
> ❌ Decision-making is inefficient  

There is a need for a **data-driven system** to support loan decisions.

---

## 💡 Solution

MARS is designed to:

- Predict loan default risk using machine learning  
- Provide a risk score and recommendation  
- Store borrower data and track outcomes  
- Support institutions in making fair and informed decisions  

---

## ⚙️ System Features

### ✅ 1. Loan Risk Prediction
- Uses trained ML model (Random Forest)
- Outputs:
  - Risk level (Low / Medium / High)
  - Probability of default

### ✅ 2. Borrower Management
- Capture borrower details:
  - Name, Gender, State
  - NIN & BVN (for identity tracking)
- Store records in database

### ✅ 3. Records & Monitoring
- View all borrowers
- Update loan outcome (Repaid / Defaulted)

### ✅ 4. Dashboard
- Total borrowers
- Number of defaulters
- Number of repaid loans
- Default rate

---

## 🧠 Machine Learning Model

- Algorithm: **Random Forest Classifier**
- Trained on cleaned loan dataset
- Features used:
  - Loan type  
  - Loan purpose  
  - Business category  
  - Loan amount  
  - Interest rate  
  - Term  
  - Income  
  - Employment type  
  - Loan history count  
  - Age  

---

## ⚖️ Ethical Considerations

To avoid bias:

- Gender and region are **excluded from model features**
- These fields are collected only for administrative purposes

---

## 🗄️ Database Design

- SQLite database (`database.db`)
- Stores:
  - Borrower information  
  - Prediction results  
  - Loan outcomes  

---

## 🖥️ User Interface

Built using **Streamlit** with multi-page navigation:

- ➕ Add Borrower  
- 📋 Records  
- 📊 Dashboard  

---

## 🏗️ Project Structure
microcredit-ai-risk-system/
│
├── app/
│ ├── streamlit_app.py
│ └── pages/
│ ├── borrower.py
│ ├── records.py
│ └── dashboard.py
│
├── model/
│ ├── modeltrain.py
│ ├── predict.py
│ └── model.pkl (ignored)
│
├── data/
│ └── cleaned_data.csv
│
├── storage/
│ ├── db_handler.py
│ └── database.db
│
├── utils/
│ └── feature_engineering.py
│
├── requirements.txt
└── README.md


---

## 🚀 How to Run the Project

### 1. Clone the Repository
https://github.com/bangiscoder/microcredit-ai-risk-system


---

### 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate


---

### 3. Install Dependencies
pip install -r requirements.txt


---

### 4. Train Model
python model/modeltrain.py


---

### 5. Run Application
python -m streamlit run app/streamlit_app.py


---

## ⚠️ Note on Model File

The trained model (`model.pkl`) is not included in the repository due to size limitations.

To regenerate the model, run:
python model/modeltrain.py


---

## 🔮 Future Improvements

- Integration with BVN/NIN APIs  
- Automatic reliability scoring from borrower history  
- Advanced dashboard visualisations  
- Deployment with persistent database (PostgreSQL)  
- Real-time model retraining  

---

## 🌍 Impact

This system aims to:

- Reduce loan default rates  
- Improve financial inclusion  
- Enable digital transformation in microcredit systems  
- Support data-driven decision making  

---

## 👤 Author

**Babangida Yohanna**  
3MTT Cohort 2 – Data Science  
Nigeria 🇳🇬

---

## 🙏 Acknowledgement

Dataset sourced from Kaggle and adapted for microcredit use case.

---
