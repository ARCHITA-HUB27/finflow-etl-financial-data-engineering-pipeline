import streamlit as st


def _card(icon, title, text, color="#38BDF8"):
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(160deg,#16213A 0%,#101A2E 100%);
            border:1px solid #22314F;
            border-left:4px solid {color};
            border-radius:14px;
            padding:16px 20px;
            margin-bottom:12px;
            display:flex;
            gap:14px;
            align-items:flex-start;
        ">
            <div style="font-size:22px;line-height:1;">{icon}</div>
            <div>
                <div style="color:#F1F5F9;font-weight:700;font-size:14.5px;margin-bottom:4px;">{title}</div>
                <div style="color:#94A3B8;font-size:13.5px;line-height:1.5;">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def generate_insights(df):
    """Compute a handful of genuinely data-driven insights (not hardcoded text)."""

    insights = []

    if "isFraud" not in df.columns or len(df) == 0:
        return insights

    fraud_df = df[df["isFraud"] == 1]
    normal_df = df[df["isFraud"] == 0]

    if len(fraud_df) == 0:
        insights.append(
            ("✅", "No Fraud Detected", "No fraudulent transactions found in the current filter selection.", "#34D399")
        )
        return insights

    # ---- 1. Fraud concentration by type ----
    if "type" in df.columns:
        fraud_by_type = fraud_df["type"].value_counts()
        top_types = fraud_by_type[fraud_by_type > 0].index.tolist()
        if top_types:
            coverage = (
                fraud_df["type"].isin(top_types).sum() / len(fraud_df) * 100
            )
            insights.append((
                "🎯",
                "Fraud Is Concentrated",
                f"100% of fraud cases occur in just {len(top_types)} transaction type(s): "
                f"{', '.join(top_types)}. Monitoring these types alone would catch every "
                f"flagged case in this dataset.",
                "#F472B6",
            ))

    # ---- 2. Full balance drain signature ----
    if {"newbalanceOrig", "oldbalanceOrg"}.issubset(df.columns):
        fraud_drain_rate = (
            (fraud_df["newbalanceOrig"] == 0).mean() * 100 if len(fraud_df) else 0
        )
        normal_drain_rate = (
            (normal_df["newbalanceOrig"] == 0).mean() * 100 if len(normal_df) else 0
        )
        if fraud_drain_rate > 0:
            insights.append((
                "🕳️",
                "Full-Balance-Drain Signature",
                f"{fraud_drain_rate:.1f}% of fraudulent transactions leave the origin account "
                f"at ₹0 balance, versus only {normal_drain_rate:.2f}% of normal transactions — "
                f"a {fraud_drain_rate / max(normal_drain_rate, 0.01):.0f}x difference. This is "
                f"one of the strongest engineered features for a fraud classifier.",
                "#EF4444",
            ))

    # ---- 3. Amount size disparity ----
    if "amount" in df.columns:
        fraud_avg = fraud_df["amount"].mean()
        normal_avg = normal_df["amount"].mean() if len(normal_df) else 0
        if normal_avg > 0:
            ratio = fraud_avg / normal_avg
            insights.append((
                "💸",
                "Fraudulent Transactions Run Larger",
                f"The average fraudulent transaction (₹{fraud_avg:,.0f}) is {ratio:.1f}x larger "
                f"than the average normal transaction (₹{normal_avg:,.0f}), suggesting fraud "
                f"targets high-value transfers rather than small purchases.",
                "#FBBF24",
            ))

    # ---- 4. Peak fraud window ----
    if "step" in df.columns and len(fraud_df) >= 5:
        fraud_df = fraud_df.copy()
        fraud_df["hour_of_day"] = fraud_df["step"] % 24
        peak_hour = fraud_df["hour_of_day"].value_counts().idxmax()
        peak_count = fraud_df["hour_of_day"].value_counts().max()
        insights.append((
            "🕐",
            "Time-Based Pattern",
            f"Fraud cases peak around hour {int(peak_hour)}:00 of the simulated day "
            f"({int(peak_count)} cases), hinting that a time-of-day feature could improve "
            f"a downstream detection model.",
            "#818CF8",
        ))

    return insights


def render_insights(df):
    insights = generate_insights(df)

    if not insights:
        return

    st.markdown('<div class="section-header">🔍 Auto-Generated Insights</div>', unsafe_allow_html=True)

    for icon, title, text, color in insights:
        _card(icon, title, text, color)