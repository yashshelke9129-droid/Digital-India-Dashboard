import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Digital India Dashboard",
    page_icon="🇮🇳",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data_file = "data/processed/digital_india_cleaned.csv"

forecast_file = "data/processed/internet_forecast.csv"

df = pd.read_csv(data_file)

forecast_df = pd.read_csv(forecast_file)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🇮🇳 Digital India Dashboard")
st.subheader("India's Digital Transformation (2016–2025)")

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.header("📌 Executive Summary")

st.info(
    """
India has undergone a remarkable digital transformation.

• Internet Usage: 27% → 75%

• Smartphone Users: 300M → 900M

• UPI Transactions: 0.02B → 160B

• GDP: $2290B → $4200B

• Literacy Rate: 74% → 79%
"""
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    df["Year"]
)

selected_metric = st.sidebar.selectbox(
    "Select Metric",
    [
        "GDP_Billion",
        "Internet_Users",
        "UPI_Billion",
        "Smartphone_Million",
        "Literacy_Rate"
    ]
)

filtered_df = df[df["Year"] == selected_year]

# --------------------------------------------------
# GROWTH CALCULATIONS
# --------------------------------------------------

gdp_growth = (
    (df["GDP_Billion"].iloc[-1] -
     df["GDP_Billion"].iloc[0])
    /
    df["GDP_Billion"].iloc[0]
) * 100

internet_growth = (
    (df["Internet_Users"].iloc[-1] -
     df["Internet_Users"].iloc[0])
    /
    df["Internet_Users"].iloc[0]
) * 100

upi_growth = (
    (df["UPI_Billion"].iloc[-1] -
     df["UPI_Billion"].iloc[0])
    /
    df["UPI_Billion"].iloc[0]
) * 100

smartphone_growth = (
    (df["Smartphone_Million"].iloc[-1] -
     df["Smartphone_Million"].iloc[0])
    /
    df["Smartphone_Million"].iloc[0]
) * 100

literacy_growth = (
    (df["Literacy_Rate"].iloc[-1] -
     df["Literacy_Rate"].iloc[0])
    /
    df["Literacy_Rate"].iloc[0]
) * 100

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "GDP",
        f"{filtered_df['GDP_Billion'].values[0]:,.0f} B",
        f"{gdp_growth:.1f}%"
    )

with col2:
    st.metric(
        "Internet %",
        f"{filtered_df['Internet_Users'].values[0]:.0f}",
        f"{internet_growth:.1f}%"
    )

with col3:
    st.metric(
        "UPI (B)",
        f"{filtered_df['UPI_Billion'].values[0]:.2f}",
        f"{upi_growth:.1f}%"
    )

with col4:
    st.metric(
        "Smartphones (M)",
        f"{filtered_df['Smartphone_Million'].values[0]:.0f}",
        f"{smartphone_growth:.1f}%"
    )

with col5:
    st.metric(
        "Literacy %",
        f"{filtered_df['Literacy_Rate'].values[0]:.1f}",
        f"{literacy_growth:.1f}%"
    )

# --------------------------------------------------
# INTERACTIVE METRIC CHART
# --------------------------------------------------

st.header("📈 Interactive Metric Analysis")

fig_metric = px.line(
    df,
    x="Year",
    y=selected_metric,
    markers=True,
    title=f"{selected_metric} Trend"
)

st.plotly_chart(fig_metric, use_container_width=True)

# --------------------------------------------------
# INTERNET USERS
# --------------------------------------------------

st.header("🌐 Internet Growth")

fig1 = px.line(
    df,
    x="Year",
    y="Internet_Users",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# GDP
# --------------------------------------------------

st.header("💰 GDP Growth")

fig2 = px.line(
    df,
    x="Year",
    y="GDP_Billion",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# UPI
# --------------------------------------------------

st.header("💳 UPI Transactions")

fig3 = px.bar(
    df,
    x="Year",
    y="UPI_Billion"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# SMARTPHONE
# --------------------------------------------------

st.header("📱 Smartphone Adoption")

fig4 = px.line(
    df,
    x="Year",
    y="Smartphone_Million",
    markers=True
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# FORECAST
# --------------------------------------------------

st.header("🔮 Internet Forecast till 2030")

forecast_fig = go.Figure()

forecast_fig.add_trace(
    go.Scatter(
        x=df["Year"],
        y=df["Internet_Users"],
        mode="lines+markers",
        name="Actual"
    )
)

forecast_fig.add_trace(
    go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Predicted_Internet"],
        mode="lines+markers",
        name="Forecast"
    )
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)

# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------

st.header("🔥 Correlation Analysis")

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="Blues",
    ax=ax
)

st.pyplot(fig)

# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

st.header("⬇ Download Dataset")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Dataset CSV",
    data=csv,
    file_name="digital_india.csv",
    mime="text/csv"
)

# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.header("📋 Dataset")

st.dataframe(df)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.header("💡 Business Insights")

st.success(
    """
1. Internet penetration increased dramatically.

2. Smartphone adoption strongly correlates with internet growth.

3. UPI recorded the fastest growth among all indicators.

4. GDP and digital transformation progressed together.

5. Literacy improvements supported digital inclusion.

6. Digital India initiatives accelerated financial technology adoption.
"""
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Yash Shelke | Digital India Dashboard Project"
)
