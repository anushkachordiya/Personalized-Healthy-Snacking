# 🥗 SnackSmart Analytics Dashboard

**AI-Powered Personalized Healthy Snacking Subscription Platform**  
*Descriptive & Diagnostic Analytics Dashboard — Project-Based Learning Assignment*

---

## 📌 Overview

This Streamlit dashboard provides a comprehensive **Descriptive and Diagnostic Analysis** of a synthetic customer dataset for **SnackSmart**, an AI-powered D2C healthy snacking subscription platform. The dashboard covers:

- Business strategy and objectives
- Raw & cleaned data exploration
- Exploratory Data Analysis (EDA) with insights
- Customer segmentation insights
- Churn & revenue diagnostics

---

## 🗂️ Project Structure

```
snack_dashboard/
│
├── app.py               # Main Streamlit application
├── data.csv             # Synthetic customer dataset (3,000 records)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🚀 Deployment on Streamlit Cloud

### Step 1 — Push to GitHub
1. Create a new GitHub repository (e.g., `snacksmart-dashboard`)
2. Upload all files from this folder into the repository root

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account and select your repository
4. Set **Main file path** to: `app.py`
5. Click **Deploy**

> ⚠️ Make sure `data.csv` is in the same directory as `app.py` in your repository.

---

## 🛠️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📊 Dashboard Tabs

| Tab | Content |
|-----|---------|
| 🏠 Business Overview | Platform concept, strategy, target segments, product categories |
| 📋 Data Overview | Raw data preview, schema, encoding key, data quality report |
| 🧹 Data Cleaning | Cleaning steps, transformations, before/after comparison |
| 📊 EDA — Customer Profile | Age, gender, income, city tier, lifestyle distributions |
| 🛒 EDA — Behaviour & Products | Spend, order frequency, preferred categories, subscriptions |
| 🔥 EDA — Churn & Value | Churn drivers, high-value customer analysis, CLV insights |
| 🔗 Correlation Analysis | Heatmap, key relationships, diagnostic insights |

---

## 🧪 Dataset Details

- **Records:** 3,000 synthetic customers
- **Features:** 20 columns covering demographics, behaviour, health goals, and business KPIs
- **Target Variables:** `Churn` (binary), `High_Value_Customer` (binary), `CLV` (continuous)

---

## 👤 Author

*Individual Project-Based Learning Assignment*  
Subject: Data Analytics  
Platform Concept: SnackSmart — AI-Powered Healthy Snacking Subscription
