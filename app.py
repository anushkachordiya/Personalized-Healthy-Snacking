import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SnackSmart Analytics",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 { font-family: 'Syne', sans-serif; }

    .main { background-color: #0f1117; }

    .hero-banner {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid #e8b86d33;
        border-radius: 16px;
        padding: 40px 48px;
        margin-bottom: 28px;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #e8b86d;
        margin: 0 0 8px 0;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #a0aec0;
        margin: 0;
    }
    .metric-card {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-val {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #e8b86d;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }
    .insight-box {
        background: linear-gradient(135deg, #1a1f2e, #16213e);
        border-left: 4px solid #e8b86d;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.93rem;
        color: #cbd5e0;
        line-height: 1.65;
    }
    .insight-box strong { color: #e8b86d; }
    .section-header {
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        border-bottom: 2px solid #e8b86d44;
        padding-bottom: 8px;
        margin: 28px 0 16px 0;
    }
    .tag {
        display: inline-block;
        background: #e8b86d22;
        border: 1px solid #e8b86d55;
        color: #e8b86d;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #1a1f2e;
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #718096;
        font-family: 'Syne', sans-serif;
        font-weight: 600;
        font-size: 0.83rem;
        padding: 8px 14px;
    }
    .stTabs [aria-selected="true"] {
        background: #e8b86d !important;
        color: #0f1117 !important;
    }
    .clean-step {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .step-num {
        font-family: 'Syne', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #e8b86d;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 4px 0;
    }
    .step-body { color: #a0aec0; font-size: 0.88rem; line-height: 1.6; }
    .warning-tag { color: #f6ad55; font-weight: 600; }
    .ok-tag { color: #68d391; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ENCODING MAPS
# ─────────────────────────────────────────────
ENCODINGS = {
    "Gender":             {0: "Male", 1: "Female"},
    "City_Tier":          {0: "Tier 1", 1: "Tier 2", 2: "Tier 3"},
    "Income_Level":       {0: "Low", 1: "Medium", 2: "High"},
    "Lifestyle_Type":     {0: "Student", 1: "Working Professional", 2: "Fitness Enthusiast"},
    "Health_Goal":        {0: "Weight Loss", 1: "Muscle Gain", 2: "General Health"},
    "Dietary_Preference": {0: "Vegan / Keto", 1: "Non-Specific"},
    "Preferred_Category": {0: "Functional Snacks", 1: "Wellness Beverages", 2: "Guilt-Free Desserts", 3: "Fitness Nutrition"},
    "Subscription_Type":  {0: "Basic", 1: "Standard", 2: "Premium"},
    "Churn":              {0: "Retained", 1: "Churned"},
    "High_Value_Customer":{0: "Standard", 1: "High Value"},
}

COLORS = {
    "primary":   "#e8b86d",
    "secondary": "#68d391",
    "danger":    "#fc8181",
    "info":      "#63b3ed",
    "purple":    "#b794f4",
    "bg":        "#1a1f2e",
    "card":      "#16213e",
}
PALETTE = ["#e8b86d","#68d391","#63b3ed","#b794f4","#fc8181","#f6ad55","#76e4f7","#fbb6ce"]

# ─────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────
@st.cache_data
def load_raw():
    return pd.read_csv("data.csv")

@st.cache_data
def load_clean():
    df = pd.read_csv("data.csv")

    # 1. Drop Customer_ID (identifier, no analytical value)
    df = df.drop(columns=["Customer_ID"])

    # 2. Decode categorical columns to readable labels
    for col, mapping in ENCODINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # 3. Cap outliers in Spend_per_Order using IQR method
    Q1 = df["Spend_per_Order"].quantile(0.25)
    Q3 = df["Spend_per_Order"].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    df["Spend_per_Order"] = df["Spend_per_Order"].clip(upper=upper)

    # 4. Cap outliers in Engagement_Score
    Q1e = df["Engagement_Score"].quantile(0.25)
    Q3e = df["Engagement_Score"].quantile(0.75)
    IQRe = Q3e - Q1e
    upper_e = Q3e + 1.5 * IQRe
    df["Engagement_Score"] = df["Engagement_Score"].clip(upper=upper_e)

    # 5. Cap CLV outliers
    Q1c = df["CLV"].quantile(0.25)
    Q3c = df["CLV"].quantile(0.75)
    IQRc = Q3c - Q1c
    upper_c = Q3c + 1.5 * IQRc
    df["CLV"] = df["CLV"].clip(upper=upper_c)

    # 6. Add derived feature: Revenue_Tier
    df["Revenue_Tier"] = pd.cut(
        df["Avg_Monthly_Spend"],
        bins=[0, 1500, 3000, 4500, 7000],
        labels=["Budget (< ₹1.5K)", "Mid (₹1.5K–3K)", "Growth (₹3K–4.5K)", "Premium (> ₹4.5K)"]
    )

    # 7. Add Age_Group
    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 60],
        labels=["18–25", "26–35", "36–45", "46–59"]
    )

    return df

raw_df  = load_raw()
clean_df = load_clean()

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-title">🥗 SnackSmart Analytics</p>
  <p class="hero-sub">AI-Powered Personalized Healthy Snacking Subscription Platform &nbsp;·&nbsp; 
     Descriptive & Diagnostic Analytics Dashboard &nbsp;·&nbsp; 3,000 Customers</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="metric-card"><div class="metric-val">3,000</div><div class="metric-label">Total Customers</div></div>', unsafe_allow_html=True)
with k2:
    avg_spend = f"₹{clean_df['Avg_Monthly_Spend'].mean():,.0f}"
    st.markdown(f'<div class="metric-card"><div class="metric-val">{avg_spend}</div><div class="metric-label">Avg Monthly Spend</div></div>', unsafe_allow_html=True)
with k3:
    churn_rate = f"{(clean_df['Churn'] == 'Churned').mean() * 100:.1f}%"
    st.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#fc8181">{churn_rate}</div><div class="metric-label">Churn Rate</div></div>', unsafe_allow_html=True)
with k4:
    hvc_rate = f"{(clean_df['High_Value_Customer'] == 'High Value').mean() * 100:.1f}%"
    st.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#68d391">{hvc_rate}</div><div class="metric-label">High-Value Customers</div></div>', unsafe_allow_html=True)
with k5:
    avg_clv = f"₹{clean_df['CLV'].mean():,.0f}"
    st.markdown(f'<div class="metric-card"><div class="metric-val">{avg_clv}</div><div class="metric-label">Avg CLV</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "🏠 Business Overview",
    "📋 Data Overview",
    "🧹 Data Cleaning",
    "👤 EDA — Customer Profile",
    "🛒 EDA — Behaviour & Products",
    "🔥 EDA — Churn & Value",
    "🔗 Correlation Analysis"
])


# ════════════════════════════════════════════
# TAB 1 — BUSINESS OVERVIEW
# ════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Platform Concept</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div class="insight-box">
        <strong>SnackSmart</strong> is a D2C (Direct-to-Consumer) AI-powered healthy snacking subscription platform 
        that delivers <strong>personalised snack boxes</strong> based on each customer's lifestyle, health goals, 
        dietary preferences, and purchase behaviour.<br><br>
        Think of it as <strong>Netflix × Swiggy Instamart × Health Tech</strong> — combining algorithmic 
        personalisation, on-demand delivery convenience, and functional nutrition science into one subscription experience.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Strategic Pillars</div>', unsafe_allow_html=True)
        for icon, title, desc in [
            ("🎯", "Hyper-Personalisation", "Snack boxes curated using AI based on real-time health goals, taste data, and behavioural patterns."),
            ("📦", "Subscription Economy", "Recurring revenue model with Basic, Standard, and Premium tiers to capture diverse willingness-to-pay."),
            ("📲", "App-Led Engagement", "Mobile-first platform driving high app usage translates directly to engagement and reduced churn."),
            ("🔄", "Retention Over Acquisition", "CLV maximisation through loyalty programs, personalised re-engagement, and churn prediction."),
            ("📊", "Data-Driven Inventory", "Association rule mining and demand forecasting prevent stockouts and overstocking."),
        ]:
            st.markdown(f"""
            <div class="clean-step">
            <div class="step-title">{icon} {title}</div>
            <div class="step-body">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Product Categories</div>', unsafe_allow_html=True)
        cats = {
            "🥗 Functional Snack Boxes": "Protein bars, keto snacks, low-carb chips",
            "🍵 Wellness Beverages":      "Detox drinks, herbal teas, kombucha",
            "🍫 Guilt-Free Desserts":     "Sugar-free chocolates, vegan desserts",
            "🏋️ Fitness Nutrition Packs": "Pre/post workout snacks, protein cookies",
        }
        for name, desc in cats.items():
            st.markdown(f"""
            <div class="clean-step">
            <div class="step-title">{name}</div>
            <div class="step-body">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Target Segments</div>', unsafe_allow_html=True)
        segments = ["🎓 Students — Budget & taste driven",
                    "💼 Working Professionals — Convenience driven",
                    "🏃 Fitness Enthusiasts — Goal driven",
                    "🩺 Diabetic / Health-Conscious — Diet specific",
                    "💎 Premium Lifestyle Users — Quality driven"]
        for s in segments:
            st.markdown(f'<span class="tag">{s}</span>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Analytics Objectives</div>', unsafe_allow_html=True)
        objectives = [
            ("📊 Descriptive", "Understand revenue distribution, segment demand, category popularity"),
            ("🔬 Diagnostic",  "Explain why customers churn, what drives high CLV, income vs spend gaps"),
            ("🤖 Predictive",  "Classify churn, predict spend, segment customers via clustering"),
            ("🛒 Prescriptive","Association rules to bundle products and personalise recommendations"),
        ]
        for label, text in objectives:
            st.markdown(f"""
            <div class="insight-box">
            <strong>{label}:</strong> {text}
            </div>
            """, unsafe_allow_html=True)

    # Analytics coverage chart
    st.markdown('<div class="section-header">Analytics Technique Coverage</div>', unsafe_allow_html=True)
    tech_df = pd.DataFrame({
        "Technique":   ["Descriptive Analytics","Diagnostic Analysis","Classification (ML)","Clustering (ML)","Association Rules","Regression (ML)"],
        "Coverage (%)": [100, 100, 85, 85, 80, 75],
        "Status":       ["✅ This Dashboard","✅ This Dashboard","🔜 Next Phase","🔜 Next Phase","🔜 Next Phase","🔜 Next Phase"]
    })
    fig = px.bar(tech_df, x="Coverage (%)", y="Technique", orientation="h",
                 color="Coverage (%)", color_continuous_scale=["#2d3748","#e8b86d"],
                 text="Status", template="plotly_dark")
    fig.update_traces(textposition="inside", textfont_size=12)
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
                      font_color="#e2e8f0", height=300,
                      margin=dict(l=0, r=20, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
# TAB 2 — DATA OVERVIEW
# ════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Raw Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(raw_df.head(20), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Dataset Schema</div>', unsafe_allow_html=True)
        schema_data = {
            "Column": raw_df.columns.tolist(),
            "Type":   [str(d) for d in raw_df.dtypes],
            "Non-Null": [raw_df[c].notna().sum() for c in raw_df.columns],
            "Unique Values": [raw_df[c].nunique() for c in raw_df.columns],
            "Category": [
                "Identifier","Demographics","Demographics","Demographics","Demographics",
                "Behavioural","Health","Health","Behavioural","Behavioural","Behavioural",
                "Behavioural","Behavioural","Behavioural","Behavioural",
                "Target Variable","Target Variable","Engineered","Target Variable","Engineered"
            ]
        }
        st.dataframe(pd.DataFrame(schema_data), use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Data Quality Report</div>', unsafe_allow_html=True)
        missing = raw_df.isnull().sum()
        duplicates = raw_df.duplicated().sum()
        st.markdown(f"""
        <div class="insight-box">
        <strong>Shape:</strong> {raw_df.shape[0]:,} rows × {raw_df.shape[1]} columns<br>
        <strong>Missing Values:</strong> <span class="ok-tag">0 — No missing values detected</span><br>
        <strong>Duplicate Rows:</strong> <span class="{'ok-tag' if duplicates == 0 else 'warning-tag'}">{duplicates} duplicates</span><br>
        <strong>Numeric Columns:</strong> {raw_df.select_dtypes(include='number').shape[1]}<br>
        <strong>Categorical (encoded):</strong> All categoricals are integer-encoded<br>
        <strong>Target Variables:</strong> Churn, High_Value_Customer (binary); CLV, Avg_Monthly_Spend (continuous)<br><br>
        <strong>Note:</strong> The dataset is synthetically generated, so it is pre-encoded. 
        Cleaning will focus on outlier treatment, decoding labels, and feature engineering.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Encoding Key</div>', unsafe_allow_html=True)
        enc_rows = []
        for col, mapping in ENCODINGS.items():
            for code, label in mapping.items():
                enc_rows.append({"Column": col, "Code": code, "Label": label})
        st.dataframe(pd.DataFrame(enc_rows), use_container_width=True, height=350)

    st.markdown('<div class="section-header">Descriptive Statistics — Raw Data</div>', unsafe_allow_html=True)
    st.dataframe(raw_df.describe().round(2), use_container_width=True)


# ════════════════════════════════════════════
# TAB 3 — DATA CLEANING
# ════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Data Cleaning & Transformation Pipeline</div>', unsafe_allow_html=True)

    steps = [
        ("STEP 1", "Drop Customer_ID Column",
         "Customer_ID is a unique row identifier with no predictive or analytical value. "
         "Including it in analysis can cause spurious correlations and inflate model complexity. "
         "It was removed before any EDA or modelling.",
         "1 column removed → 20 → 19 columns"),
        ("STEP 2", "Decode Categorical Columns",
         "All categorical variables were originally label-encoded as integers (0, 1, 2…) for storage efficiency. "
         "Decoding them back to their original string labels (e.g., 0 → 'Male', 1 → 'Female') makes the data "
         "human-readable, ensures correct visualisation, and prevents the model from treating them as ordinal numbers "
         "when they are nominal categories.",
         "10 columns decoded: Gender, City_Tier, Income_Level, Lifestyle_Type, Health_Goal, Dietary_Preference, "
         "Preferred_Category, Subscription_Type, Churn, High_Value_Customer"),
        ("STEP 3", "Outlier Capping — Spend_per_Order (IQR Method)",
         "Spend_per_Order had extreme right-skewed outliers (max ₹3,262 vs median ₹253). These are likely data "
         "anomalies in a synthetic dataset. Using the IQR method (Upper Fence = Q3 + 1.5×IQR), all values above "
         "the fence were capped to preserve the distribution shape without deleting rows.",
         "Values above the upper fence were capped. No rows deleted."),
        ("STEP 4", "Outlier Capping — Engagement_Score (IQR Method)",
         "Engagement_Score showed values up to 2,223 with a median of 489 — a stark right tail. "
         "These extreme values would distort visualisations and correlations. IQR capping was applied "
         "to bring the scale to a realistic operational range.",
         "Upper outliers capped. Distribution normalised."),
        ("STEP 5", "Outlier Capping — CLV (IQR Method)",
         "Customer Lifetime Value ranged from ₹3,270 to ₹858,762 — an extremely wide range. "
         "While high CLV customers exist, the extreme outliers in a synthetic dataset can mislead regression models "
         "and summary statistics. IQR capping retains genuine high-value customers while removing anomalies.",
         "CLV capped at upper IQR fence. Mean CLV re-stabilised."),
        ("STEP 6", "Feature Engineering — Revenue_Tier",
         "A new categorical column was derived from Avg_Monthly_Spend using business-aligned bins: "
         "Budget (< ₹1.5K), Mid (₹1.5K–₹3K), Growth (₹3K–₹4.5K), Premium (> ₹4.5K). "
         "This enables segment-level revenue analysis without treating spend as continuous in every chart.",
         "New column added: Revenue_Tier (4 categories)"),
        ("STEP 7", "Feature Engineering — Age_Group",
         "Age was binned into generational cohorts (18–25, 26–35, 36–45, 46–59) to enable "
         "demographic segmentation analysis. This is more meaningful for business strategy than raw age values.",
         "New column added: Age_Group (4 categories)"),
    ]

    for step_num, step_title, step_body, step_result in steps:
        st.markdown(f"""
        <div class="clean-step">
        <div class="step-num">{step_num}</div>
        <div class="step-title">{step_title}</div>
        <div class="step-body">{step_body}<br><br>
        <span class="ok-tag">→ Result:</span> {step_result}
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Outlier Analysis — Before vs After Capping</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    for col_widget, col_name in zip([col1, col2, col3], ["Spend_per_Order", "Engagement_Score", "CLV"]):
        with col_widget:
            raw_vals   = raw_df[col_name]
            clean_vals = clean_df[col_name]
            fig = go.Figure()
            fig.add_trace(go.Box(y=raw_vals,   name="Raw",   marker_color=COLORS["danger"],    boxmean=True))
            fig.add_trace(go.Box(y=clean_vals, name="Cleaned", marker_color=COLORS["secondary"], boxmean=True))
            fig.update_layout(title=col_name, template="plotly_dark",
                              plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                              font_color="#e2e8f0", height=300,
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Cleaned Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(clean_df.head(20), use_container_width=True)
    st.markdown(f"**Shape after cleaning:** {clean_df.shape[0]:,} rows × {clean_df.shape[1]} columns")
    st.dataframe(clean_df.describe(include="all").round(2), use_container_width=True)


# ════════════════════════════════════════════
# TAB 4 — EDA: CUSTOMER PROFILE
# ════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Demographic Distribution Overview</div>', unsafe_allow_html=True)

    # Row 1: Age distribution + Gender
    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.histogram(clean_df, x="Age", nbins=30, color_discrete_sequence=[COLORS["primary"]],
                           title="Age Distribution of Customers",
                           template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", bargap=0.05,
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>What it shows:</strong> The age distribution is spread between 18–59 years with a roughly 
        uniform spread across the range, indicating synthetic generation across all adult cohorts.<br>
        <strong>Trend:</strong> No dominant age spike — the platform attracts customers across all adult age groups.<br>
        <strong>Business Insight:</strong> Marketing cannot be age-specific alone; lifestyle and health goals 
        are stronger segmentation drivers than raw age.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        gender_counts = clean_df["Gender"].value_counts().reset_index()
        fig = px.pie(gender_counts, values="count", names="Gender",
                     color_discrete_sequence=[COLORS["info"], COLORS["primary"]],
                     title="Gender Split", template="plotly_dark", hole=0.55)
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=0, r=0, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Near-equal male-female split (~49% / 51%). 
        Gender is not a strong differentiator for this platform — product and communication 
        personalisation should lean on health goals rather than gender.
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Lifestyle + Income
    col1, col2 = st.columns(2)
    with col1:
        lf_counts = clean_df["Lifestyle_Type"].value_counts().reset_index()
        fig = px.bar(lf_counts, x="Lifestyle_Type", y="count",
                     color="Lifestyle_Type", color_discrete_sequence=PALETTE,
                     title="Customer Lifestyle Distribution", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>What it shows:</strong> Almost equal split across Students (995), Working Professionals (982), 
        and Fitness Enthusiasts (1,023).<br>
        <strong>Trend:</strong> Fitness Enthusiasts are the slightly dominant segment (~34%), 
        closely followed by Students and Working Professionals.<br>
        <strong>Business Insight:</strong> SnackSmart's <strong>Fitness Nutrition</strong> and 
        <strong>Functional Snack</strong> categories are well-positioned for the largest segment. 
        Targeted bundles for Working Professionals (convenience) and Students (price-sensitive) should be distinct.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        inc_counts = clean_df["Income_Level"].value_counts().reset_index()
        fig = px.bar(inc_counts, x="Income_Level", y="count",
                     color="Income_Level", color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="Income Level Distribution", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>What it shows:</strong> High-income customers dominate (1,606 out of 3,000 — over 53%), 
        followed by Medium (863) and Low (531).<br>
        <strong>Trend:</strong> The platform skews toward high-income users, suggesting effective 
        positioning as a premium health product.<br>
        <strong>Business Insight:</strong> The large High-income segment validates a <strong>premium tier subscription</strong>. 
        However, capturing the Low-income segment (students) requires budget-friendly plans.
        </div>
        """, unsafe_allow_html=True)

    # Row 3: City Tier + Age Group
    col1, col2 = st.columns(2)
    with col1:
        city_counts = clean_df["City_Tier"].value_counts().reset_index()
        fig = px.bar(city_counts, x="count", y="City_Tier", orientation="h",
                     color="City_Tier", color_discrete_sequence=PALETTE,
                     title="Customer Distribution by City Tier", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=40))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Tier 1 cities dominate (1,523 customers — 51%). Tier 3 has the fewest (602 — 20%).<br>
        <strong>Business Insight:</strong> Metro cities (Tier 1) are the core market, driven by higher disposable 
        income and health awareness. However, Tier 2 (875 customers) is a significant emerging market 
        where health consciousness is rising — a key <strong>growth opportunity</strong>.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        age_grp = clean_df["Age_Group"].value_counts().reset_index()
        fig = px.bar(age_grp, x="Age_Group", y="count",
                     color="Age_Group", color_discrete_sequence=PALETTE,
                     title="Customer Distribution by Age Group", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> The 36–45 age group is largest, followed closely by 26–35 and 46–59. 
        The 18–25 segment is the smallest.<br>
        <strong>Business Insight:</strong> The core customer is a <strong>mid-career adult (26–45)</strong> 
        who is health-conscious and financially capable. Gen-Z acquisition (18–25) is an opportunity via 
        student pricing and social-media campaigns.
        </div>
        """, unsafe_allow_html=True)

    # Row 4: Health Goal + Dietary Preference
    col1, col2 = st.columns(2)
    with col1:
        hg_counts = clean_df["Health_Goal"].value_counts().reset_index()
        fig = px.pie(hg_counts, values="count", names="Health_Goal",
                     color_discrete_sequence=PALETTE, hole=0.5,
                     title="Health Goal Distribution", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=0, r=0, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Near-equal split — Muscle Gain (34.3%), Weight Loss (33.1%), 
        General Health (32.6%). No single goal dominates.<br>
        <strong>Business Insight:</strong> The platform must maintain a balanced product portfolio. 
        <strong>Personalisation</strong> is critical — the same customer base has three very different 
        nutritional needs requiring distinct snack formulations.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        dp_counts = clean_df["Dietary_Preference"].value_counts().reset_index()
        fig = px.pie(dp_counts, values="count", names="Dietary_Preference",
                     color_discrete_sequence=[COLORS["secondary"], COLORS["primary"]], hole=0.5,
                     title="Dietary Preference Split", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=0, r=0, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> 70% of customers have Non-Specific dietary preferences; 
        30% follow Vegan/Keto diets.<br>
        <strong>Business Insight:</strong> While the majority have flexible diets, a significant 
        30% require <strong>specialised product lines</strong>. Vegan/Keto SKUs must be clearly labelled 
        and curated separately to retain this high-intent, premium segment.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 5 — EDA: BEHAVIOUR & PRODUCTS
# ════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Spending & Ordering Behaviour</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(clean_df, x="Avg_Monthly_Spend", nbins=40,
                           color_discrete_sequence=[COLORS["primary"]],
                           title="Average Monthly Spend Distribution (₹)",
                           template="plotly_dark")
        fig.add_vline(x=clean_df["Avg_Monthly_Spend"].mean(), line_dash="dash",
                      line_color=COLORS["secondary"], annotation_text=f"Mean ₹{clean_df['Avg_Monthly_Spend'].mean():,.0f}")
        fig.add_vline(x=clean_df["Avg_Monthly_Spend"].median(), line_dash="dot",
                      line_color=COLORS["info"], annotation_text=f"Median ₹{clean_df['Avg_Monthly_Spend'].median():,.0f}")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>What it shows:</strong> Monthly spend ranges from ₹502 to ₹6,524 with a mean of ~₹2,793.<br>
        <strong>Trend:</strong> Right-skewed distribution — most customers spend ₹1,500–₹3,500, but a tail 
        of high spenders exists (>₹5,000).<br>
        <strong>Business Insight:</strong> The ₹1,500–₹3,500 band is the <strong>sweet spot for pricing</strong>. 
        Premium boxes above ₹4,500 target a smaller but high-value segment worth investing in.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = px.histogram(clean_df, x="Order_Frequency", nbins=20,
                           color_discrete_sequence=[COLORS["info"]],
                           title="Order Frequency per Month",
                           template="plotly_dark")
        fig.add_vline(x=clean_df["Order_Frequency"].mean(), line_dash="dash",
                      line_color=COLORS["primary"], annotation_text=f"Mean {clean_df['Order_Frequency'].mean():.1f} orders")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>What it shows:</strong> Customers order between 1–19 times per month. 
        Mean is ~9.3 orders/month.<br>
        <strong>Trend:</strong> Roughly bell-shaped, centred around 7–12 orders — consistent with 
        weekly snacking behaviour.<br>
        <strong>Business Insight:</strong> High-frequency buyers (>15 orders/month) are power users 
        — excellent candidates for <strong>unlimited snack plans</strong> or loyalty rewards.
        </div>
        """, unsafe_allow_html=True)

    # Revenue Tier
    col1, col2 = st.columns(2)
    with col1:
        tier_counts = clean_df["Revenue_Tier"].value_counts().reset_index().sort_values("Revenue_Tier")
        fig = px.bar(tier_counts, x="Revenue_Tier", y="count",
                     color="Revenue_Tier", color_discrete_sequence=PALETTE,
                     title="Customer Count by Revenue Tier", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> The largest segment is Mid-tier (₹1.5K–3K), followed by Budget. 
        Premium spenders (>₹4.5K) are a small but critical group.<br>
        <strong>Business Insight:</strong> A tiered subscription model (Basic→Premium) should align 
        with these natural spending bands. <strong>Upsell nudges</strong> from Mid to Growth tier 
        offer the highest revenue growth opportunity.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        spend_tier = clean_df.groupby("Revenue_Tier", observed=True)["Avg_Monthly_Spend"].mean().reset_index()
        fig = px.bar(spend_tier, x="Revenue_Tier", y="Avg_Monthly_Spend",
                     color="Revenue_Tier", color_discrete_sequence=PALETTE,
                     title="Avg Monthly Spend by Revenue Tier (₹)", template="plotly_dark",
                     text=spend_tier["Avg_Monthly_Spend"].round(0))
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Preferred Category + Subscription
    st.markdown('<div class="section-header">Product & Subscription Preferences</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        pc_counts = clean_df["Preferred_Category"].value_counts().reset_index()
        fig = px.bar(pc_counts, x="count", y="Preferred_Category", orientation="h",
                     color="Preferred_Category", color_discrete_sequence=PALETTE,
                     title="Preferred Product Category", template="plotly_dark", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Fitness Nutrition Packs (1,023) and Functional Snacks (995) are the 
        most popular. Wellness Beverages and Guilt-Free Desserts are secondary preferences.<br>
        <strong>Business Insight:</strong> <strong>Protein and performance nutrition</strong> is the 
        dominant demand. Guilt-Free Desserts and Beverages serve as cross-sell / bundle opportunities 
        for high-frequency buyers.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        sub_counts = clean_df["Subscription_Type"].value_counts().reset_index()
        fig = px.pie(sub_counts, values="count", names="Subscription_Type",
                     color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="Subscription Type Distribution", template="plotly_dark", hole=0.5)
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=0, r=0, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Basic (45%) dominates, followed by Premium (40%) and Standard (14.5%).<br>
        <strong>Business Insight:</strong> The <strong>missing middle (Standard tier)</strong> is undersubscribed. 
        This is a typical subscription "barbell effect." Improving the Standard tier's value proposition 
        could capture upgrade revenue from Basic subscribers.
        </div>
        """, unsafe_allow_html=True)

    # Spend by Category and Subscription
    col1, col2 = st.columns(2)
    with col1:
        spend_cat = clean_df.groupby("Preferred_Category")["Avg_Monthly_Spend"].mean().reset_index()
        fig = px.bar(spend_cat, x="Preferred_Category", y="Avg_Monthly_Spend",
                     color="Preferred_Category", color_discrete_sequence=PALETTE,
                     title="Avg Monthly Spend by Category (₹)", template="plotly_dark",
                     text=spend_cat["Avg_Monthly_Spend"].round(0))
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Business Insight:</strong> Categories with similar average spend suggest the 
        spend driver is more about <strong>Income Level and Subscription Type</strong> than product category. 
        Bundle pricing should reflect the customer's plan, not just the category.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        spend_sub = clean_df.groupby("Subscription_Type")["Avg_Monthly_Spend"].mean().reset_index()
        fig = px.bar(spend_sub, x="Subscription_Type", y="Avg_Monthly_Spend",
                     color="Subscription_Type",
                     color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="Avg Monthly Spend by Subscription (₹)", template="plotly_dark",
                     text=spend_sub["Avg_Monthly_Spend"].round(0))
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> Premium subscribers spend significantly more than Basic and Standard.<br>
        <strong>Business Insight:</strong> <strong>Premium plan conversion is the highest-ROI lever</strong> 
        for revenue growth. Each upsell from Basic to Premium nearly doubles the monthly revenue per customer.
        </div>
        """, unsafe_allow_html=True)

    # App Usage
    st.markdown('<div class="section-header">App Engagement</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(clean_df, x="App_Usage_Time", nbins=30,
                           color_discrete_sequence=[COLORS["purple"]],
                           title="App Usage Time Distribution (mins/day)",
                           template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> App usage is uniformly spread 5–119 mins/day. Mean ~63 mins/day — 
        indicating high daily engagement for a snacking app.<br>
        <strong>Business Insight:</strong> High app time correlates with high Engagement Score (r=0.70). 
        <strong>In-app nudges and personalised notifications</strong> have a large captive audience to work with.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = px.box(clean_df, x="Subscription_Type", y="App_Usage_Time",
                     color="Subscription_Type",
                     color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="App Usage Time by Subscription Type", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Business Insight:</strong> App usage is fairly similar across subscription tiers — 
        meaning <strong>engagement is platform-wide</strong>, not just a premium behaviour. 
        This is positive for conversion: Basic-tier users are already engaged and primed for upsell.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 6 — EDA: CHURN & VALUE
# ════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Churn Analysis</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    total = len(clean_df)
    churned = (clean_df["Churn"] == "Churned").sum()
    retained = total - churned
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#fc8181">{churned:,}</div><div class="metric-label">Churned Customers</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#68d391">{retained:,}</div><div class="metric-label">Retained Customers</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{churned/total*100:.1f}%</div><div class="metric-label">Churn Rate</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Churn by key segments
    col1, col2 = st.columns(2)
    with col1:
        churn_income = clean_df.groupby("Income_Level")["Churn"].apply(
            lambda x: (x == "Churned").mean() * 100).reset_index()
        churn_income.columns = ["Income_Level", "Churn Rate (%)"]
        fig = px.bar(churn_income, x="Income_Level", y="Churn Rate (%)",
                     color="Churn Rate (%)", color_continuous_scale=["#68d391","#fc8181"],
                     title="Churn Rate by Income Level (%)", template="plotly_dark",
                     text=churn_income["Churn Rate (%)"].round(1))
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          coloraxis_showscale=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Low-income customers churn significantly more (~38%) than High-income 
        customers (~24%). This is a classic price-sensitivity churn signal.<br>
        <strong>Diagnosis:</strong> Budget constraints force low-income customers to cancel subscriptions 
        when financial pressure hits.<br>
        <strong>Action:</strong> Introduce <strong>pause-instead-of-cancel</strong> options and 
        budget flex plans for low-income segments.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        churn_sub = clean_df.groupby("Subscription_Type")["Churn"].apply(
            lambda x: (x == "Churned").mean() * 100).reset_index()
        churn_sub.columns = ["Subscription_Type", "Churn Rate (%)"]
        fig = px.bar(churn_sub, x="Subscription_Type", y="Churn Rate (%)",
                     color="Churn Rate (%)", color_continuous_scale=["#68d391","#fc8181"],
                     title="Churn Rate by Subscription Type (%)", template="plotly_dark",
                     text=churn_sub["Churn Rate (%)"].round(1))
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          coloraxis_showscale=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Basic subscribers have the highest churn rate. 
        Premium subscribers are the most loyal.<br>
        <strong>Diagnosis:</strong> Low investment in a plan = low commitment and perceived value.<br>
        <strong>Action:</strong> Offer <strong>trial upgrades and personalised feature unlocks</strong> 
        to Basic subscribers after 2 months to build switching costs.
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        churn_lifestyle = clean_df.groupby("Lifestyle_Type")["Churn"].apply(
            lambda x: (x == "Churned").mean() * 100).reset_index()
        churn_lifestyle.columns = ["Lifestyle_Type", "Churn Rate (%)"]
        fig = px.bar(churn_lifestyle, x="Lifestyle_Type", y="Churn Rate (%)",
                     color="Lifestyle_Type", color_discrete_sequence=PALETTE,
                     title="Churn Rate by Lifestyle Type (%)", template="plotly_dark",
                     text=churn_lifestyle["Churn Rate (%)"].round(1))
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Spend vs Churn box
        fig = px.box(clean_df, x="Churn", y="Avg_Monthly_Spend",
                     color="Churn",
                     color_discrete_map={"Churned": COLORS["danger"], "Retained": COLORS["secondary"]},
                     title="Monthly Spend Distribution: Churned vs Retained", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Churned customers have a noticeably lower median monthly spend 
        compared to retained customers.<br>
        <strong>Diagnosis:</strong> Low spend = lower perceived value delivered = higher churn likelihood. 
        This validates spend as a leading indicator of churn risk.
        </div>
        """, unsafe_allow_html=True)

    # Churn by Discount Sensitivity
    st.markdown('<div class="section-header">Discount Sensitivity & Churn</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(clean_df, x="Discount_Sensitivity", color="Churn",
                           color_discrete_map={"Churned": COLORS["danger"], "Retained": COLORS["secondary"]},
                           barmode="overlay", title="Discount Sensitivity by Churn Status",
                           template="plotly_dark", nbins=20, opacity=0.75)
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Churned customers tend to have higher discount sensitivity scores, 
        meaning they rely more on promotions.<br>
        <strong>Diagnosis:</strong> Discount-dependent customers are <strong>price-loyal, not brand-loyal</strong>. 
        When discounts dry up, they leave.<br>
        <strong>Action:</strong> Shift high-discount-sensitivity customers toward <strong>value-added loyalty 
        programs</strong> (exclusive products, early access) rather than price cuts.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = px.box(clean_df, x="Churn", y="Order_Frequency",
                     color="Churn",
                     color_discrete_map={"Churned": COLORS["danger"], "Retained": COLORS["secondary"]},
                     title="Order Frequency: Churned vs Retained", template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Churned customers have lower order frequency than retained ones.<br>
        <strong>Diagnosis:</strong> Frequency is a strong behavioural signal — customers who order less 
        frequently are disengaging before they formally cancel.<br>
        <strong>Action:</strong> Build a <strong>declining-frequency alert</strong> in the platform 
        to trigger personalised re-engagement flows 2–3 weeks before churn becomes likely.
        </div>
        """, unsafe_allow_html=True)

    # CLV & High Value Analysis
    st.markdown('<div class="section-header">Customer Lifetime Value (CLV) & High-Value Customers</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(clean_df, x="CLV", nbins=40,
                           color_discrete_sequence=[COLORS["primary"]],
                           title="CLV Distribution (₹)", template="plotly_dark")
        fig.add_vline(x=clean_df["CLV"].mean(), line_dash="dash",
                      line_color=COLORS["secondary"],
                      annotation_text=f"Mean ₹{clean_df['CLV'].mean():,.0f}")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> CLV is right-skewed — most customers cluster in lower CLV ranges, 
        while a small group drives disproportionate lifetime value.<br>
        <strong>Business Insight:</strong> Classic <strong>Pareto pattern</strong> — focus retention 
        efforts on the high-CLV tail. Losing one high-CLV customer costs as much as losing 5–10 average customers.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        clv_income = clean_df.groupby("Income_Level")["CLV"].mean().reset_index()
        fig = px.bar(clv_income, x="Income_Level", y="CLV",
                     color="Income_Level",
                     color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="Avg CLV by Income Level (₹)", template="plotly_dark",
                     text=clv_income["CLV"].round(0))
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Trend:</strong> High-income customers generate dramatically higher CLV than Low-income ones.<br>
        <strong>Business Insight:</strong> Acquiring high-income customers has a <strong>compounding ROI</strong>. 
        Premium acquisition channels (influencer partnerships, corporate wellness programs) 
        that target high-income segments are justified by CLV.
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        hvc_sub = clean_df.groupby("Subscription_Type")["High_Value_Customer"].apply(
            lambda x: (x == "High Value").mean() * 100).reset_index()
        hvc_sub.columns = ["Subscription_Type", "HVC Rate (%)"]
        fig = px.bar(hvc_sub, x="Subscription_Type", y="HVC Rate (%)",
                     color="Subscription_Type",
                     color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["secondary"]],
                     title="% High-Value Customers by Subscription Type", template="plotly_dark",
                     text=hvc_sub["HVC Rate (%)"].round(1))
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Premium subscribers have the highest concentration of High-Value Customers.<br>
        <strong>Business Insight:</strong> <strong>Subscription tier is the strongest signal of customer value.</strong> 
        Premium tier acquisition and retention should receive disproportionate investment.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = px.box(clean_df, x="High_Value_Customer", y="Engagement_Score",
                     color="High_Value_Customer",
                     color_discrete_map={"Standard": COLORS["info"], "High Value": COLORS["primary"]},
                     title="Engagement Score: Standard vs High-Value Customers",
                     template="plotly_dark")
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          showlegend=False, font_color="#e2e8f0",
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        <strong>Key Finding:</strong> Engagement scores for Standard and High-Value customers overlap significantly.<br>
        <strong>Diagnosis:</strong> Engagement alone does not predict customer value — 
        <strong>spend and order frequency</strong> are stronger value signals than app time.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 7 — CORRELATION ANALYSIS
# ════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">Correlation Heatmap — Numeric Features</div>', unsafe_allow_html=True)

    numeric_cols = clean_df.select_dtypes(include="number").columns.tolist()
    corr = clean_df[numeric_cols].corr()

    fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                    color_continuous_scale=["#fc8181","#1a1f2e","#68d391"],
                    zmin=-1, zmax=1,
                    title="Pearson Correlation Matrix",
                    template="plotly_dark")
    fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                      font_color="#e2e8f0", height=600,
                      margin=dict(l=10, r=10, t=50, b=10))
    fig.update_traces(textfont_size=9)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>How to read this:</strong> Values closer to +1 (green) indicate a strong positive relationship; 
    values closer to -1 (red) indicate a strong negative relationship; values near 0 (dark) indicate no linear relationship.
    </div>
    """, unsafe_allow_html=True)

    # Key relationships
    st.markdown('<div class="section-header">Key Correlation Findings & Diagnostic Insights</div>', unsafe_allow_html=True)

    findings = [
        ("🟢 Strong Positive", "Avg_Monthly_Spend ↔ High_Value_Customer", "+0.77",
         "Monthly spend is the single strongest predictor of customer value. High-spend customers are overwhelmingly flagged as high-value. "
         "This validates spend-based segmentation as the primary business KPI."),
        ("🟢 Strong Positive", "Avg_Monthly_Spend ↔ CLV", "+0.71",
         "Customers who spend more monthly naturally accumulate higher lifetime value. "
         "This compounding effect means retaining high-spend customers is exponentially more valuable than acquiring new low-spend ones."),
        ("🟢 Strong Positive", "Order_Frequency ↔ CLV", "+0.61",
         "Frequent buyers build high lifetime value. This makes Order Frequency a leading indicator — "
         "a rise in order frequency predicts future CLV growth, and a decline signals pre-churn disengagement."),
        ("🟢 Strong Positive", "App_Usage_Time ↔ Engagement_Score", "+0.70",
         "App usage is the dominant driver of engagement. More time on-app correlates directly with higher engagement scores. "
         "This supports heavy investment in in-app experience and push notification strategies."),
        ("🟢 Strong Positive", "Order_Frequency ↔ Engagement_Score", "+0.64",
         "Frequent buyers are more engaged — or engagement drives more orders. "
         "This bidirectional relationship supports gamification and loyalty programs to boost both metrics simultaneously."),
        ("🔴 Strong Negative", "Income_Level ↔ High_Value_Customer", "-0.69",
         "Counter-intuitive at first: lower income codes are numerically smaller (0=Low, 2=High), "
         "so this confirms High-Income customers (code 2) are NOT classified as High-Value in higher numbers — "
         "rather, <strong>High Value is driven by spend behaviour, not income label</strong>. "
         "A high-income customer who doesn't spend is not high-value."),
        ("🔴 Moderate Negative", "Avg_Monthly_Spend ↔ Subscription_Type", "-0.48",
         "Lower subscription codes (Basic=0) correlate with lower spend. Basic subscribers spend less — "
         "confirming that <strong>plan type directly constrains and reflects spending capacity</strong>."),
        ("🔴 Moderate Negative", "Order_Frequency ↔ Spend_per_Order", "-0.56",
         "Customers who order frequently tend to spend less per order — they may be buying smaller, habitual snack packs. "
         "High-value customers order less frequently but spend more per order — suggesting <strong>premium bundle purchases</strong>."),
        ("🟡 Moderate Positive", "Avg_Monthly_Spend ↔ Spend_per_Order", "+0.57",
         "Customers with higher monthly spend also spend more per individual order — "
         "confirming that high-spend customers are not just ordering more times but are buying premium products."),
        ("⚪ Near Zero", "Age ↔ Most Variables", "~0.0",
         "Age shows almost no linear correlation with spend, churn, CLV, or engagement. "
         "This confirms that <strong>lifestyle and income, not age, are the real segmentation drivers</strong> for SnackSmart."),
    ]

    for color, pair, value, insight in findings:
        st.markdown(f"""
        <div class="clean-step">
        <div class="step-num">{color} &nbsp;&nbsp; Correlation: <strong style="color:#e8b86d">{value}</strong></div>
        <div class="step-title">{pair}</div>
        <div class="step-body">{insight}</div>
        </div>
        """, unsafe_allow_html=True)

    # Scatter plots for top correlations
    st.markdown('<div class="section-header">Key Relationship Scatter Plots</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(clean_df.sample(500, random_state=42),
                         x="Avg_Monthly_Spend", y="CLV",
                         color="Subscription_Type",
                         color_discrete_sequence=PALETTE,
                         title="Monthly Spend vs CLV (sample n=500)",
                         template="plotly_dark", opacity=0.65)
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(clean_df.sample(500, random_state=42),
                         x="Order_Frequency", y="Engagement_Score",
                         color="Churn",
                         color_discrete_map={"Churned": COLORS["danger"], "Retained": COLORS["secondary"]},
                         title="Order Frequency vs Engagement Score (sample n=500)",
                         template="plotly_dark", opacity=0.65)
        fig.update_layout(plot_bgcolor=COLORS["bg"], paper_bgcolor=COLORS["bg"],
                          font_color="#e2e8f0", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Scatter — Spend vs CLV:</strong> Clear positive linear trend, with Premium subscribers 
    clustered in the high-spend, high-CLV quadrant. Basic subscribers spread across the lower range.<br><br>
    <strong>Scatter — Order Frequency vs Engagement:</strong> Retained customers cluster in the 
    high-frequency, high-engagement zone. Churned customers are concentrated in the low-frequency, 
    low-engagement zone — making this quadrant a <strong>churn early-warning signal</strong>.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#4a5568; font-size:0.82rem; padding: 10px 0 20px 0;">
    🥗 <strong style="color:#e8b86d">SnackSmart Analytics Dashboard</strong> &nbsp;·&nbsp; 
    Built with Streamlit & Plotly &nbsp;·&nbsp; 
    Data Analytics Project-Based Learning Assignment &nbsp;·&nbsp;
    Descriptive & Diagnostic Analysis
</div>
""", unsafe_allow_html=True)
