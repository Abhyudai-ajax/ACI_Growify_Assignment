-- =====================================================
-- ADVANCED AI DIMENSIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_creative (
    creative_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creative_name TEXT,
    creative_format TEXT,
    creative_type TEXT,
    hook_style TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_audience (
    audience_id INTEGER PRIMARY KEY AUTOINCREMENT,
    audience_type TEXT,
    interest_cluster TEXT,
    geo_segment TEXT,
    customer_persona TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SAFE INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_campaign_date
ON fact_campaign_performance(date);

CREATE INDEX IF NOT EXISTS idx_campaign_funnel
ON dim_campaign(funnel_stage);

-- =====================================================
-- AI ANALYTICS VIEWS
-- =====================================================

CREATE VIEW IF NOT EXISTS v_ai_creative_performance AS
SELECT
    creative_id,
    AVG(roas) as avg_roas,
    AVG(ctr) as avg_ctr,
    AVG(cvr) as avg_cvr,
    SUM(spend) as total_spend,
    SUM(revenue) as total_revenue
FROM fact_campaign_performance
GROUP BY creative_id;

CREATE VIEW IF NOT EXISTS v_ai_audience_performance AS
SELECT
    audience_id,
    AVG(roas) as avg_roas,
    AVG(cpc) as avg_cpc,
    AVG(cvr) as avg_cvr,
    SUM(spend) as total_spend
FROM fact_campaign_performance
GROUP BY audience_id;