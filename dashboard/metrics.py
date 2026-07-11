import streamlit as st
from utils import format_currency, format_number, safe_ratio


def metric_card(title, value, icon, glow_color="#38BDF8", delta=None, delta_color="#34D399"):

    delta_html = ""
    if delta:
        delta_html = f'<div class="metric-delta" style="color:{delta_color};">{delta}</div>'

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="glow" style="background:{glow_color};"></div>
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_metrics(df):

    total_transactions = len(df)
    fraud_transactions = int(df["isFraud"].sum()) if "isFraud" in df.columns else 0
    fraud_rate = safe_ratio(fraud_transactions, total_transactions)

    total_amount = df["amount"].sum() if "amount" in df.columns else 0
    avg_amount = df["amount"].mean() if "amount" in df.columns and total_transactions else 0

    fraud_amount = (
        df.loc[df["isFraud"] == 1, "amount"].sum()
        if "isFraud" in df.columns and "amount" in df.columns
        else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        metric_card(
            "Transactions",
            format_number(total_transactions),
            "📊",
            glow_color="#38BDF8",
        )

    with c2:
        metric_card(
            "Fraud Cases",
            format_number(fraud_transactions),
            "🚨",
            glow_color="#EF4444",
            delta=f"{fraud_rate:.2f}% of total",
            delta_color="#F87171",
        )

    with c3:
        risk_label = "Low" if fraud_rate < 1 else ("Moderate" if fraud_rate < 5 else "High")
        risk_color = "#34D399" if fraud_rate < 1 else ("#FBBF24" if fraud_rate < 5 else "#F87171")
        metric_card(
            "Fraud Rate",
            f"{fraud_rate:.2f}%",
            "⚠️",
            glow_color=risk_color,
            delta=f"{risk_label} risk",
            delta_color=risk_color,
        )

    with c4:
        metric_card(
            "Total Volume",
            format_currency(total_amount),
            "💰",
            glow_color="#818CF8",
        )

    with c5:
        metric_card(
            "Fraud Exposure",
            format_currency(fraud_amount),
            "🛡️",
            glow_color="#F472B6",
            delta=f"Avg txn {format_currency(avg_amount)}",
            delta_color="#94A3B8",
        )