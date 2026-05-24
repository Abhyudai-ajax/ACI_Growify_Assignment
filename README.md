# 🚀 Growify AI Marketing Intelligence Platform

AI-powered analytics engineering platform for campaign optimization, funnel intelligence, audience analytics, and marketing decision intelligence.

Built as part of the Growify Digital Data Analyst + AI Developer Assignment.

---

# 📌 Project Overview

Growify AI Marketing Intelligence Platform is a complete end-to-end analytics engineering system designed to:

- clean and process raw marketing datasets
- build a dimensional data warehouse
- generate advanced campaign intelligence
- analyze marketing funnels
- detect performance anomalies
- recommend optimization actions
- provide interactive AI-powered dashboards

The platform combines:
- Data Engineering
- SQL Warehousing
- Analytics Engineering
- AI Insight Systems
- Interactive Business Intelligence

---

# ✨ Core Features

## ✅ Data Engineering Pipeline
- Automated ETL workflow
- Raw campaign ingestion
- Shopify sales processing
- Null handling & normalization
- KPI transformations
- Logging & reporting

---

## ✅ Marketing Intelligence Engine
- ROAS analysis
- CTR / CPC / CPM analytics
- Funnel leak detection
- Audience intelligence
- Creative performance scoring
- Campaign optimization insights

---

## ✅ AI Recommendation Engine
The platform automatically recommends:

- ✅ SCALE
- ⚠️ OPTIMIZE
- ❌ PAUSE

based on campaign performance metrics.

---

## ✅ Interactive AI Dashboard
Built using:
- Streamlit
- Plotly
- SQLite

Dashboard includes:
- Executive KPI layer
- Campaign analytics
- Audience insights
- Funnel visualization
- Creative intelligence
- AI recommendations

---

# 🧠 Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Database | SQLite |
| Data Processing | Pandas |
| Visualization | Plotly |
| Dashboarding | Streamlit |
| Warehousing | SQL |
| Analytics | KPI Engineering |
| AI Architecture | Text-to-SQL Design |

---

# 🏗️ Warehouse Architecture

The platform uses a:

# ⭐ Star Schema Warehouse

## Fact Tables
- `fact_campaign_performance`

## Dimension Tables
- `dim_campaign`
- `dim_creative`
- `dim_audience`
- `dim_date`

## Analytics Views
- Campaign ROI Views
- Funnel Analysis Views
- Executive KPI Views
- AI Insight Views

---

# 📊 Key Marketing Metrics

The system calculates:

- ROAS
- CTR
- CPC
- CPM
- CVR
- Revenue
- Spend
- Funnel Performance
- Audience ROI

---

# 🤖 AI Intelligence Features

## Creative Intelligence
Analyzes:
- best performing creatives
- revenue contribution
- creative format impact

## Audience Intelligence
Analyzes:
- geo performance
- audience segments
- customer personas

## Funnel Leak Detection
Detects:
- high CTR + low CVR campaigns
- funnel inefficiencies
- conversion bottlenecks

## Action Recommendation Engine
Automatically suggests:
- scale winning campaigns
- pause underperforming campaigns
- optimize weak funnels

---

# 📁 Project Structure

```bash
Growify_AI_Platform/
│
├── data/
│   ├── cleaned/
│   ├── database/
│   ├── reports/
│   ├── campaigns_raw.csv
│   └── Shopify_Raw.csv
│
├── python/
│   ├── data_cleaner.py
│   ├── ai_insight_tool.py
│   ├── ai_insight_tool_v2.py
│   └── dashboard.py
│
├── sql/
│   ├── schema.sql
│   ├── migration_v2.sql
│   └── populate_warehouse.sql
│
├── logs/
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── POWER_BI_SETUP.md