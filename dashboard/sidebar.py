import streamlit as st


def apply_filters(df):

    st.sidebar.markdown("### ⚙️ Filters")
    st.sidebar.caption("Refine the dataset in real time")

    filtered = df.copy()

    # ---------------- Transaction type ----------------

    if "type" in df.columns:
        types = sorted(df["type"].unique().tolist())
        transaction_types = st.sidebar.multiselect(
            "Transaction Type",
            options=types,
            default=types,
        )
        filtered = filtered[filtered["type"].isin(transaction_types)]

    # ---------------- Fraud status ----------------

    if "isFraud" in df.columns:
        fraud_status = st.sidebar.selectbox(
            "Fraud Status",
            ["All", "Fraud Only", "Non-Fraud Only"],
        )

        if fraud_status == "Fraud Only":
            filtered = filtered[filtered["isFraud"] == 1]
        elif fraud_status == "Non-Fraud Only":
            filtered = filtered[filtered["isFraud"] == 0]

    # ---------------- Amount range ----------------

    if "amount" in df.columns and len(df) > 0:
        min_amt = float(df["amount"].min())
        max_amt = float(df["amount"].max())

        if min_amt < max_amt:
            amt_range = st.sidebar.slider(
                "Transaction Amount (₹)",
                min_value=min_amt,
                max_value=max_amt,
                value=(min_amt, max_amt),
            )
            filtered = filtered[
                (filtered["amount"] >= amt_range[0])
                & (filtered["amount"] <= amt_range[1])
            ]

    # ---------------- Time step range ----------------

    if "step" in df.columns and len(df) > 0:
        min_step = int(df["step"].min())
        max_step = int(df["step"].max())

        if min_step < max_step:
            step_range = st.sidebar.slider(
                "Time Step",
                min_value=min_step,
                max_value=max_step,
                value=(min_step, max_step),
            )
            filtered = filtered[
                (filtered["step"] >= step_range[0])
                & (filtered["step"] <= step_range[1])
            ]

    st.sidebar.markdown("---")
    st.sidebar.metric("Rows in view", f"{len(filtered):,}", f"of {len(df):,} total")

    if st.sidebar.button("🔄 Reset Filters", width="stretch"):
        st.rerun()

    return filtered