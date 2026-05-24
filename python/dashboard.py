import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Growify AI Intelligence Platform",
    layout="wide"
)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "data/database/cleaned_campaigns.db"
)

# =====================================================
# LOAD DATA
# =====================================================

fact_df = pd.read_sql_query(
    "SELECT * FROM fact_campaign_performance",
    conn
)

campaign_df = pd.read_sql_query(
    "SELECT * FROM dim_campaign",
    conn
)

creative_df = pd.read_sql_query(
    "SELECT * FROM dim_creative",
    conn
)

audience_df = pd.read_sql_query(
    "SELECT * FROM dim_audience",
    conn
)

# =====================================================
# MERGE DATA
# =====================================================

df = fact_df.merge(
    campaign_df,
    on="campaign_id",
    how="left",
    suffixes=("", "_campaign")
)

df = df.merge(
    creative_df,
    on="creative_id",
    how="left",
    suffixes=("", "_creative")
)

df = df.merge(
    audience_df,
    on="audience_id",
    how="left",
    suffixes=("", "_aud")
)

# =====================================================
# HEADER
# =====================================================

st.title("🚀 Growify AI Marketing Intelligence Platform")

st.markdown("""
### AI-powered analytics engineering platform for:
- Campaign Intelligence
- Funnel Analytics
- Creative Scoring
- Audience Insights
- Action Recommendations
""")

# =====================================================
# KPI SECTION
# =====================================================

total_revenue = round(df["revenue"].sum(), 2)
total_spend = round(df["spend"].sum(), 2)
avg_roas = round(df["roas"].mean(), 2)
avg_ctr = round(df["ctr"].mean(), 2)
avg_cvr = round(df["cvr"].mean(), 2)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Spend", f"₹{total_spend:,.0f}")
col3.metric("Avg ROAS", avg_roas)
col4.metric("Avg CTR", f"{avg_ctr}%")
col5.metric("Avg CVR", f"{avg_cvr}%")

st.divider()

# =====================================================
# TOP CAMPAIGNS
# =====================================================

st.subheader("📈 Top Campaigns by ROAS")

campaign_perf = (
    df.groupby("campaign_name")["roas"]
    .mean()
    .reset_index()
    .sort_values(by="roas", ascending=False)
    .head(10)
)

fig = px.bar(
    campaign_perf,
    x="campaign_name",
    y="roas",
    color="roas",
    title="Top Campaign ROAS"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CREATIVE PERFORMANCE
# =====================================================

st.subheader("🎨 Creative Intelligence")

creative_perf = (
    df.groupby("creative_format")["revenue"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    creative_perf,
    names="creative_format",
    values="revenue",
    title="Revenue by Creative Format"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# AUDIENCE PERFORMANCE
# =====================================================

st.subheader("🧠 Audience Intelligence")

audience_perf = (
    df.groupby("geo_segment")["revenue"]
    .sum()
    .reset_index()
)

fig3 = px.treemap(
    audience_perf,
    path=["geo_segment"],
    values="revenue",
    title="Revenue by Audience Geography"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# FUNNEL ANALYSIS
# =====================================================

st.subheader("⚠️ Funnel Leak Detection")

funnel_df = (
    df.groupby("campaign_name")[["ctr", "cvr"]]
    .mean()
    .reset_index()
)

fig4 = px.scatter(
    funnel_df,
    x="ctr",
    y="cvr",
    hover_name="campaign_name",
    color="ctr",
    title="CTR vs CVR Funnel Analysis"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# ACTION ENGINE
# =====================================================

st.subheader("🤖 AI Action Recommendation Engine")

for _, row in campaign_perf.iterrows():

    if row["roas"] >= 3:
        action = "✅ SCALE"

    elif row["roas"] < 1:
        action = "❌ PAUSE"

    else:
        action = "⚠️ OPTIMIZE"

    st.write(
        f"{action} → {row['campaign_name']} "
        f"(ROAS: {round(row['roas'], 2)})"
    )



# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### ✅ Project Features
- AI Marketing Intelligence
- Data Warehouse Engineering
- Funnel Analytics
- Audience Intelligence
- Creative Scoring
- Recommendation Engine
- Interactive Dashboard
""")