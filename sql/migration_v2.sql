-- =====================================================
-- ADD ADVANCED MARKETING COLUMNS
-- =====================================================

ALTER TABLE fact_campaign_performance
ADD COLUMN revenue DECIMAL(12,2);

ALTER TABLE fact_campaign_performance
ADD COLUMN roas DECIMAL(8,2);

ALTER TABLE fact_campaign_performance
ADD COLUMN cvr DECIMAL(8,2);

ALTER TABLE fact_campaign_performance
ADD COLUMN creative_id INTEGER;

ALTER TABLE fact_campaign_performance
ADD COLUMN audience_id INTEGER;

ALTER TABLE dim_campaign
ADD COLUMN funnel_stage TEXT;

-- =====================================================
-- CREATE NEW DIMENSIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_creative (
    creative_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creative_name TEXT,
    creative_format TEXT,
    creative_type TEXT,
    hook_style TEXT
);

CREATE TABLE IF NOT EXISTS dim_audience (
    audience_id INTEGER PRIMARY KEY AUTOINCREMENT,
    audience_type TEXT,
    interest_cluster TEXT,
    geo_segment TEXT,
    customer_persona TEXT
);