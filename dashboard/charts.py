import streamlit as st
import plotly.express as px
import pandas as pd

DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E2E8F0",
    margin=dict(t=60, b=30, l=10, r=10),
    legend=dict(font=dict(color="#E2E8F0")),
)


def _style(fig, title_x=0.05):
    fig.update_layout(**DARK_LAYOUT, title_x=title_x)
    return fig


def show_distribution_charts(df):
    """Transaction-type pie + fraud-vs-normal donut, side by side."""

    col1, col2 = st.columns(2)

    with col1:
        if "type" in df.columns:
            pie_data = df["type"].value_counts().reset_index()
            pie_data.columns = ["Transaction Type", "Count"]

            fig = px.pie(
                pie_data,
                names="Transaction Type",
                values="Count",
                hole=0.60,
                color_discrete_sequence=px.colors.qualitative.Bold,
                title="Transaction Type Distribution",
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>",
            )
            st.plotly_chart(_style(fig, 0.28), width="stretch")

    with col2:
        if "isFraud" in df.columns:
            fraud = df["isFraud"].value_counts().reset_index()
            fraud.columns = ["Fraud", "Count"]
            fraud["Fraud"] = fraud["Fraud"].replace({0: "Normal", 1: "Fraud"})

            fig2 = px.pie(
                fraud,
                names="Fraud",
                values="Count",
                hole=0.60,
                color="Fraud",
                color_discrete_map={"Normal": "#10B981", "Fraud": "#EF4444"},
                title="Fraud vs Normal Transactions",
            )
            fig2.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>",
            )
            st.plotly_chart(_style(fig2, 0.30), width="stretch")


def show_fraud_rate_by_type(df):
    """Horizontal bar showing fraud rate (%) per transaction type - key insight chart."""

    if "type" not in df.columns or "isFraud" not in df.columns:
        return

    grouped = (
        df.groupby("type")["isFraud"]
        .agg(["sum", "count"])
        .reset_index()
    )
    grouped["Fraud Rate (%)"] = (grouped["sum"] / grouped["count"] * 100).round(3)
    grouped = grouped.sort_values("Fraud Rate (%)", ascending=True)

    fig = px.bar(
        grouped,
        x="Fraud Rate (%)",
        y="type",
        orientation="h",
        text="Fraud Rate (%)",
        color="Fraud Rate (%)",
        color_continuous_scale=["#10B981", "#FBBF24", "#EF4444"],
        title="Fraud Rate by Transaction Type",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Fraud Rate (%)")
    st.plotly_chart(_style(fig, 0.35), width="stretch")


def show_amount_histogram(chart_df):

    if "amount" not in chart_df.columns:
        return

    log_scale = st.checkbox("Log scale", value=True, key="hist_log_scale")

    fig = px.histogram(
        chart_df,
        x="amount",
        nbins=60,
        title="Transaction Amount Distribution",
        color_discrete_sequence=["#38BDF8"],
        log_y=log_scale,
    )
    fig.update_layout(bargap=0.05, xaxis_title="Amount (₹)", yaxis_title="Count (log)" if log_scale else "Count")
    st.plotly_chart(_style(fig, 0.32), width="stretch")


def show_fraud_scatter(chart_df):
    """Scatter of origin balance vs amount, colored by fraud - reveals fraud patterns."""

    required = {"amount", "oldbalanceOrg", "isFraud"}
    if not required.issubset(chart_df.columns):
        return

    plot_df = chart_df.copy()
    plot_df["Status"] = plot_df["isFraud"].map({0: "Normal", 1: "Fraud"})

    zoom = st.checkbox(
        "Zoom to typical transaction range (99th percentile)",
        value=True,
        key="scatter_zoom",
    )

    # draw Normal points first, Fraud points last so they render on top
    plot_df = plot_df.sort_values("isFraud")

    fig = px.scatter(
        plot_df,
        x="oldbalanceOrg",
        y="amount",
        color="Status",
        color_discrete_map={"Normal": "#10B981", "Fraud": "#EF4444"},
        opacity=0.6,
        title="Transaction Amount vs Origin Balance (Fraud Pattern)",
        labels={"oldbalanceOrg": "Origin Account Balance (₹)", "amount": "Transaction Amount (₹)"},
        category_orders={"Status": ["Normal", "Fraud"]},
    )
    fig.update_traces(
        marker=dict(size=6),
        selector=dict(name="Normal"),
    )
    fig.update_traces(
        marker=dict(size=9, line=dict(width=1, color="#FCA5A5")),
        selector=dict(name="Fraud"),
    )

    if zoom and len(plot_df):
        x_cap = plot_df["oldbalanceOrg"].quantile(0.99)
        y_cap = plot_df["amount"].quantile(0.99)
        fig.update_xaxes(range=[0, max(x_cap, 1)])
        fig.update_yaxes(range=[0, max(y_cap, 1)])

    st.plotly_chart(_style(fig, 0.16), width="stretch")


def show_drain_rate_chart(df):
    """Compares how often fraud vs normal transactions fully drain the origin
    account - one of the strongest fraud signatures in PaySim-style data."""

    required = {"newbalanceOrig", "isFraud"}
    if not required.issubset(df.columns) or len(df) == 0:
        return

    rates = (
        df.assign(Drained=df["newbalanceOrig"] == 0)
        .groupby("isFraud")["Drained"]
        .mean()
        .mul(100)
        .reset_index()
    )
    rates["Status"] = rates["isFraud"].map({0: "Normal", 1: "Fraud"})

    fig = px.bar(
        rates,
        x="Status",
        y="Drained",
        color="Status",
        text="Drained",
        color_discrete_map={"Normal": "#10B981", "Fraud": "#EF4444"},
        title="Full-Balance-Drain Rate: Fraud vs Normal",
        labels={"Drained": "% of Transactions Draining Account to ₹0"},
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="% Fully Drained")
    st.plotly_chart(_style(fig, 0.20), width="stretch")


def show_time_series(df):
    """Transaction volume over time steps, split by fraud status."""

    if "step" not in df.columns or "isFraud" not in df.columns:
        return

    ts = (
        df.groupby(["step", "isFraud"])
        .size()
        .reset_index(name="Count")
    )
    ts["Status"] = ts["isFraud"].map({0: "Normal", 1: "Fraud"})

    fig = px.line(
        ts,
        x="step",
        y="Count",
        color="Status",
        color_discrete_map={"Normal": "#38BDF8", "Fraud": "#EF4444"},
        title="Transaction Volume Over Time",
        labels={"step": "Time Step (hours)"},
    )
    st.plotly_chart(_style(fig, 0.30), width="stretch")


def show_charts(filtered_df, chart_df):
    """Render the full chart suite for the dashboard."""

    show_distribution_charts(filtered_df)

    col1, col2 = st.columns(2)
    with col1:
        show_fraud_rate_by_type(filtered_df)
    with col2:
        show_amount_histogram(chart_df)

    show_fraud_scatter(chart_df)

    col3, col4 = st.columns(2)
    with col3:
        show_drain_rate_chart(filtered_df)
    with col4:
        show_time_series(filtered_df)