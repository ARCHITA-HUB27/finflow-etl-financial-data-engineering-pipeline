import os
import base64

import numpy as np
import pandas as pd
import streamlit as st

from styles import load_css
from metrics import show_metrics
from sidebar import apply_filters
from charts import show_charts
from insights import render_insights
from utils import format_currency

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FinFlow Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(load_css(), unsafe_allow_html=True)

# ---------------- DATA LOADING ----------------


def _find_csv():
    """Look for the transactions CSV in a few likely locations."""

    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "data", "processed", "cleaned_transactions.csv"),
        os.path.join(here, "data", "cleaned_transactions.csv"),
        os.path.join(os.path.dirname(here), "data", "processed", "cleaned_transactions.csv"),
        os.path.join(here, "cleaned_transactions.csv"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


@st.cache_data(show_spinner="Loading transaction data...")
def generate_synthetic_data(n_rows=25000, seed=42):
    """Generate a PaySim-style synthetic fraud dataset so the dashboard
    always runs, even without the original data file."""

    rng = np.random.default_rng(seed)

    types = rng.choice(
        ["CASH_OUT", "PAYMENT", "CASH_IN", "TRANSFER", "DEBIT"],
        size=n_rows,
        p=[0.35, 0.34, 0.22, 0.08, 0.01],
    )

    amount = np.round(rng.lognormal(mean=9.0, sigma=1.4, size=n_rows), 2)
    step = rng.integers(1, 744, size=n_rows)

    old_balance_org = np.round(np.clip(rng.lognormal(mean=9.5, sigma=1.6, size=n_rows), 0, None), 2)
    new_balance_org = np.round(np.clip(old_balance_org - amount, 0, None), 2)

    old_balance_dest = np.round(np.clip(rng.lognormal(mean=8.5, sigma=1.8, size=n_rows), 0, None), 2)
    new_balance_dest = np.round(old_balance_dest + amount, 2)

    fraud_prone = np.isin(types, ["TRANSFER", "CASH_OUT"])
    high_amount = amount > np.quantile(amount, 0.97)
    fraud_prob = np.where(fraud_prone & high_amount, 0.35, 0.0006)
    is_fraud = (rng.random(n_rows) < fraud_prob).astype(int)

    df = pd.DataFrame(
        {
            "step": step,
            "type": types,
            "amount": amount,
            "nameOrig": [f"C{n}" for n in rng.integers(10**8, 10**9, size=n_rows)],
            "oldbalanceOrg": old_balance_org,
            "newbalanceOrig": new_balance_org,
            "nameDest": [f"M{n}" for n in rng.integers(10**8, 10**9, size=n_rows)],
            "oldbalanceDest": old_balance_dest,
            "newbalanceDest": new_balance_dest,
            "isFraud": is_fraud,
            "isFlaggedFraud": 0,
        }
    )

    return df.sort_values("step").reset_index(drop=True)


@st.cache_data(show_spinner="Loading transaction data...")
def load_data(csv_path):
    return pd.read_csv(csv_path)


csv_path = _find_csv()
using_synthetic = csv_path is None

if using_synthetic:
    df = generate_synthetic_data()
else:
    try:
        df = load_data(csv_path)
    except Exception:
        using_synthetic = True
        df = generate_synthetic_data()

# ---------------- SIDEBAR ----------------

filtered_df = apply_filters(df)

# ---------------- SAMPLE FOR HEAVY CHARTS ----------------

sample_size = min(50000, len(filtered_df))
chart_df = (
    filtered_df.sample(sample_size, random_state=42)
    if len(filtered_df) > sample_size
    else filtered_df.copy()
)

# ---------------- HEADER ----------------

st.markdown('<div class="main-title">💳 FinFlow Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Real-Time Financial Fraud Detection Dashboard</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="live-pill">
        <span><span class="live-dot"></span>LIVE MONITORING</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------- METRICS ----------------

show_metrics(filtered_df)

st.write("")

# ---------------- TABS ----------------

tab_overview, tab_fraud, tab_data = st.tabs(
    ["📈 Overview", "🚨 Fraud Deep Dive", "📋 Data Explorer"]
)

with tab_overview:
    render_insights(filtered_df)
    st.write("")
    st.markdown('<div class="section-header">Transaction Landscape</div>', unsafe_allow_html=True)
    show_charts(filtered_df, chart_df)

with tab_fraud:
    st.markdown('<div class="section-header">Fraud Summary by Type</div>', unsafe_allow_html=True)

    if "type" in filtered_df.columns and "isFraud" in filtered_df.columns:
        summary = (
            filtered_df.groupby("type", as_index=False)
            .agg(
                Total_Transactions=("type", "count"),
                Fraud_Cases=("isFraud", "sum"),
                Total_Amount=("amount", "sum"),
                Average_Amount=("amount", "mean"),
            )
        )
        summary["Fraud Rate (%)"] = (
            summary["Fraud_Cases"] / summary["Total_Transactions"] * 100
        ).round(3)
        summary["Total Amount"] = summary["Total_Amount"].apply(format_currency)
        summary["Average Amount"] = summary["Average_Amount"].apply(format_currency)

        summary = summary.rename(
            columns={"type": "Transaction Type", "Total_Transactions": "Transactions", "Fraud_Cases": "Fraud Cases"}
        )[
            ["Transaction Type", "Transactions", "Fraud Cases", "Fraud Rate (%)", "Total Amount", "Average Amount"]
        ]

        st.dataframe(summary, width="stretch", height=230)

    st.markdown('<div class="section-header">Top Flagged Transactions</div>', unsafe_allow_html=True)

    if "isFraud" in filtered_df.columns:
        top_fraud = (
            filtered_df[filtered_df["isFraud"] == 1]
            .sort_values("amount", ascending=False)
            .head(20)
        )
        if len(top_fraud):
            st.dataframe(top_fraud, width="stretch", height=350)
        else:
            st.success("No fraud transactions in the current filter selection. ✅")

with tab_data:
    st.markdown('<div class="section-header">Sample Transactions</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df.head(500), width="stretch", height=450)

    st.write("")
    st.markdown('<div class="section-header">Export Data</div>', unsafe_allow_html=True)

    export_df = filtered_df.head(50000)
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_bytes,
        file_name="filtered_transactions.csv",
        mime="text/csv",
    )

st.markdown(
    '<div class="footer-caption">FinFlow ETL Pipeline • Python • Pandas • Streamlit • Plotly</div>',
    unsafe_allow_html=True,
)