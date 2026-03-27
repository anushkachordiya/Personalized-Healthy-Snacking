
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("AI Healthy Snack Business Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Business Objective", "Raw & Clean Data", "EDA", "Insights"])

with tab1:
    st.header("Business Objective & Strategy")
    st.write("""
    This business focuses on personalized healthy snack subscriptions.
    Objective: Use data-driven insights to improve targeting, retention, and revenue.
    Strategy:
    - Segment customers
    - Reduce churn
    - Increase engagement
    """)

with tab2:
    st.header("Dataset Overview")
    st.subheader("Raw Data")
    st.dataframe(df.head())

    st.subheader("Cleaning Steps")
    st.write("""
    - Filled missing values using mode
    - Treated outliers using IQR
    - Encoded categorical variables
    - Created Spend_per_Order feature
    """)

with tab3:
    st.header("Exploratory Data Analysis")

    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), ax=ax)
    st.pyplot(fig)

    st.write("Insight: Spend strongly correlates with CLV.")

    st.subheader("Income vs Spend")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df['Income_Level'], y=df['Avg_Monthly_Spend'], ax=ax2)
    st.pyplot(fig2)

    st.write("Insight: Higher income leads to higher spending.")

    st.subheader("Churn Distribution")
    fig3, ax3 = plt.subplots()
    sns.countplot(x=df['Churn'], ax=ax3)
    st.pyplot(fig3)

    st.write("Insight: Majority customers retained, churn still significant.")

with tab4:
    st.header("Business Insights")
    st.write("""
    - High income customers drive revenue
    - Engagement increases frequency
    - Low spend customers likely to churn
    """)

