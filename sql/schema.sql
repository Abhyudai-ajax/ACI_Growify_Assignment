-- ============================================================================
-- GROWIFY DIGITAL - SQL SCHEMA & QUERIES
-- Data Analyst + AI Developer Assignment
-- Purpose: Single source of truth for Power BI and AI tool
-- Architecture: Star Schema (Fact + Dimensions)
-- ============================================================================

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- Date Dimension Table
-- Purpose: Enables time-based analysis and proper date relationships
-- Why: Separate date dimension allows Power BI to build proper date hierarchies
-- (Year → Quarter → Month → Week → Day)
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date_value TEXT NOT NULL UNIQUE,
    day_of_week INTEGER,
    day_of_month INTEGER,
    week_of_year INTEGER,
    month INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes on date dimension for fast lookups
CREATE INDEX idx_dim_date_value ON dim_date(date_value);
CREATE INDEX idx_dim_date_month_year ON dim_date(year, month);
CREATE INDEX idx_dim_date_quarter ON dim_date(year, quarter);

-- Campaign Dimension Table
-- Purpose: Store all campaign metadata (relatively static)
CREATE TABLE dim_campaign (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    platform TEXT NOT NULL,  -- facebook, google, instagram, etc.
    channel TEXT NOT NULL,   -- cpc, cpa, display, search, social, etc.
    region TEXT NOT NULL,    -- uk, us, eu, asia, etc.
    status TEXT NOT NULL,    -- active, paused, completed
    start_date TEXT,
    end_date TEXT,
    budget_allocated DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes on campaign dimension for filtering
CREATE INDEX idx_dim_campaign_platform ON dim_campaign(platform);
CREATE INDEX idx_dim_campaign_channel ON dim_campaign(channel);
CREATE INDEX idx_dim_campaign_region ON dim_campaign(region);
CREATE INDEX idx_dim_campaign_status ON dim_campaign(status);
CREATE INDEX idx_dim_campaign_name ON dim_campaign(campaign_name);

-- Product/Conversion Dimension
-- Purpose: Store product and conversion metadata
CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_category TEXT,
    region TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FACT TABLES
-- ============================================================================

-- Campaign Performance Fact Table
-- Purpose: Store granular campaign metrics (impressions, clicks, spend, conversions)
-- Design: One row per campaign per day (daily aggregation)
-- Why: Enables efficient aggregation and analysis
CREATE TABLE fact_campaign_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    spend DECIMAL(12, 2) DEFAULT 0,
    ctr DECIMAL(5, 2) DEFAULT 0,
    cpc DECIMAL(8, 2) DEFAULT 0,
    cpm DECIMAL(8, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (campaign_id) REFERENCES dim_campaign(campaign_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    
    -- Uniqueness: Only one record per campaign per day
    UNIQUE(campaign_id, date_id)
);

-- Create indexes for frequent filtering patterns
CREATE INDEX idx_fact_campaign_date ON fact_campaign_performance(date_id);
CREATE INDEX idx_fact_campaign_campaign_id ON fact_campaign_performance(campaign_id);
CREATE INDEX idx_fact_campaign_date_range ON fact_campaign_performance(date_id, campaign_id);

-- Sales/Conversion Fact Table
-- Purpose: Detailed sales transactions
-- Design: One row per transaction/conversion
CREATE TABLE fact_shopify_sales (
    sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL UNIQUE,
    date_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    campaign_id INTEGER,  -- Link to campaign if applicable
    quantity INTEGER DEFAULT 1,
    revenue DECIMAL(12, 2) NOT NULL,
    discount DECIMAL(12, 2) DEFAULT 0,
    net_revenue DECIMAL(12, 2) GENERATED ALWAYS AS (revenue - discount) STORED,
    customer_region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (campaign_id) REFERENCES dim_campaign(campaign_id)
);

-- Create indexes for sales analysis
CREATE INDEX idx_fact_sales_date ON fact_shopify_sales(date_id);
CREATE INDEX idx_fact_sales_campaign ON fact_shopify_sales(campaign_id);
CREATE INDEX idx_fact_sales_product ON fact_shopify_sales(product_id);
CREATE INDEX idx_fact_sales_region ON fact_shopify_sales(customer_region);

-- ============================================================================
-- MATERIALIZED VIEWS FOR POWER BI
-- ============================================================================

-- View 1: Campaign Performance by Month
-- Purpose: Power BI uses this for monthly trend analysis
-- Why: Pre-aggregation improves Power BI performance
CREATE VIEW v_campaign_performance_monthly AS
SELECT
    c.campaign_id,
    c.campaign_name,
    c.platform,
    c.channel,
    c.region,
    d.year,
    d.month,
    d.quarter,
    SUM(f.impressions) AS total_impressions,
    SUM(f.clicks) AS total_clicks,
    SUM(f.conversions) AS total_conversions,
    SUM(f.spend) AS total_spend,
    ROUND(AVG(f.ctr), 2) AS avg_ctr,
    ROUND(AVG(f.cpc), 2) AS avg_cpc,
    ROUND(AVG(f.cpm), 2) AS avg_cpm,
    COUNT(DISTINCT f.date_id) AS days_active
FROM fact_campaign_performance f
INNER JOIN dim_campaign c ON f.campaign_id = c.campaign_id
INNER JOIN dim_date d ON f.date_id = d.date_id
GROUP BY
    c.campaign_id, c.campaign_name, c.platform, c.channel, c.region,
    d.year, d.month, d.quarter;

-- View 2: Sales Performance by Region & Date
-- Purpose: Regional sales analysis for Power BI
CREATE VIEW v_sales_performance_regional AS
SELECT
    d.year,
    d.month,
    d.quarter,
    d.date_value,
    s.customer_region AS region,
    p.product_category,
    COUNT(s.sales_id) AS transaction_count,
    SUM(s.quantity) AS total_quantity,
    SUM(s.revenue) AS total_revenue,
    SUM(s.discount) AS total_discount,
    SUM(s.net_revenue) AS net_revenue,
    ROUND(AVG(s.revenue), 2) AS avg_transaction_value
FROM fact_shopify_sales s
INNER JOIN dim_date d ON s.date_id = d.date_id
INNER JOIN dim_product p ON s.product_id = p.product_id
GROUP BY
    d.year, d.month, d.quarter, d.date_value,
    s.customer_region, p.product_category;

-- View 3: Campaign ROI Analysis
-- Purpose: Calculate ROI for each campaign
-- Why: Enables ROI ranking and performance comparison
CREATE VIEW v_campaign_roi AS
SELECT
    c.campaign_id,
    c.campaign_name,
    c.platform,
    c.channel,
    c.region,
    SUM(f.spend) AS total_spend,
    SUM(s.net_revenue) AS total_revenue,
    CASE
        WHEN SUM(f.spend) > 0 THEN
            ROUND(((SUM(s.net_revenue) - SUM(f.spend)) / SUM(f.spend)) * 100, 2)
        ELSE 0
    END AS roi_percent,
    CASE
        WHEN SUM(f.spend) > 0 THEN
            ROUND(SUM(s.net_revenue) / SUM(f.spend), 2)
        ELSE 0
    END AS roas,
    SUM(f.conversions) AS total_conversions,
    SUM(s.quantity) AS units_sold
FROM fact_campaign_performance f
LEFT JOIN fact_shopify_sales s ON f.campaign_id = s.campaign_id
INNER JOIN dim_campaign c ON f.campaign_id = c.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.platform, c.channel, c.region;

-- ============================================================================
-- QUERY TEMPLATES FOR POWER BI
-- ============================================================================

-- Query 1: Executive Summary KPIs
-- Purpose: Top-level metrics for Executive Summary page
-- Usage: Power BI connects to this query
CREATE VIEW v_powerbi_executive_summary AS
SELECT
    'Total Spend' AS metric_name,
    SUM(spend) AS metric_value,
    'currency' AS metric_type
FROM fact_campaign_performance
UNION ALL
SELECT
    'Total Conversions' AS metric_name,
    SUM(conversions) AS metric_value,
    'number' AS metric_type
FROM fact_campaign_performance
UNION ALL
SELECT
    'Total Revenue' AS metric_name,
    SUM(net_revenue) AS metric_value,
    'currency' AS metric_type
FROM fact_shopify_sales
UNION ALL
SELECT
    'Avg CTR %' AS metric_name,
    ROUND(AVG(ctr), 2) AS metric_value,
    'percent' AS metric_type
FROM fact_campaign_performance;

-- Query 2: Campaign Performance by Platform & Channel
-- Purpose: Drill-down analysis for Channel Breakdown page
CREATE VIEW v_powerbi_platform_channel AS
SELECT
    c.platform,
    c.channel,
    COUNT(DISTINCT c.campaign_id) AS campaign_count,
    SUM(f.impressions) AS total_impressions,
    SUM(f.clicks) AS total_clicks,
    SUM(f.conversions) AS total_conversions,
    SUM(f.spend) AS total_spend,
    ROUND(AVG(f.ctr), 2) AS avg_ctr,
    ROUND(AVG(f.cpc), 2) AS avg_cpc,
    ROUND(SUM(s.net_revenue) / NULLIF(SUM(f.spend), 0), 2) AS roas
FROM fact_campaign_performance f
INNER JOIN dim_campaign c ON f.campaign_id = c.campaign_id
LEFT JOIN fact_shopify_sales s ON f.campaign_id = s.campaign_id
GROUP BY c.platform, c.channel
ORDER BY total_spend DESC;

-- Query 3: Regional Performance Matrix
-- Purpose: Country-wise/region-wise performance comparison
CREATE VIEW v_powerbi_regional_matrix AS
SELECT
    c.region,
    c.platform,
    COUNT(DISTINCT c.campaign_id) AS campaigns,
    SUM(f.spend) AS total_spend,
    SUM(f.conversions) AS conversions,
    ROUND(SUM(s.net_revenue) / NULLIF(SUM(f.spend), 0), 2) AS roas,
    ROUND(100 * SUM(f.conversions) / NULLIF(SUM(f.clicks), 0), 2) AS conversion_rate
FROM fact_campaign_performance f
INNER JOIN dim_campaign c ON f.campaign_id = c.campaign_id
LEFT JOIN fact_shopify_sales s ON f.campaign_id = s.campaign_id
GROUP BY c.region, c.platform
ORDER BY total_spend DESC;

-- ============================================================================
-- FLEXIBLE QUERY TEMPLATE FOR AI TOOL
-- ============================================================================

-- Template: Dynamic Campaign Analysis
-- Purpose: AI tool uses this base query and filters by user question
-- Parameters: date_from, date_to, platform, region, campaign_name
CREATE VIEW v_ai_campaign_analysis AS
SELECT
    d.date_value,
    d.year,
    d.month,
    d.quarter,
    c.campaign_id,
    c.campaign_name,
    c.platform,
    c.channel,
    c.region,
    f.impressions,
    f.clicks,
    f.conversions,
    f.spend,
    f.ctr,
    f.cpc,
    f.cpm,
    s.revenue,
    s.net_revenue,
    s.quantity,
    ROUND(s.net_revenue / NULLIF(f.spend, 0), 2) AS daily_roas,
    ROUND(100 * f.conversions / NULLIF(f.clicks, 0), 2) AS conversion_rate
FROM fact_campaign_performance f
INNER JOIN dim_campaign c ON f.campaign_id = c.campaign_id
INNER JOIN dim_date d ON f.date_id = d.date_id
LEFT JOIN fact_shopify_sales s ON f.campaign_id = s.campaign_id
    AND f.date_id = s.date_id;

-- Template: Sales Analysis for AI
-- Purpose: Flexible sales queries for natural language questions
CREATE VIEW v_ai_sales_analysis AS
SELECT
    d.date_value,
    d.year,
    d.month,
    d.quarter,
    s.product_id,
    p.product_name,
    p.product_category,
    s.customer_region,
    s.quantity,
    s.revenue,
    s.discount,
    s.net_revenue,
    c.campaign_name,
    c.platform
FROM fact_shopify_sales s
INNER JOIN dim_date d ON s.date_id = d.date_id
INNER JOIN dim_product p ON s.product_id = p.product_id
LEFT JOIN dim_campaign c ON s.campaign_id = c.campaign_id;

-- ============================================================================
-- INDEX SUMMARY & RATIONALE
-- ============================================================================
-- idx_dim_date_value: Fast date lookups (WHERE date = '2024-01-15')
-- idx_dim_date_month_year: Monthly/yearly aggregations
-- idx_dim_campaign_platform/channel/region: Common filter dimensions
-- idx_fact_campaign_date_range: Date range queries (WHERE date BETWEEN X AND Y)
-- idx_fact_sales_region: Regional sales analysis
-- 
-- These indexes are designed for:
-- 1. Power BI filter operations (platform, region, date)
-- 2. AI tool question filtering (date ranges, regions, campaigns)
-- 3. Aggregation queries (GROUP BY platform, channel, region, date)

-- ============================================================================
-- DATA LOADING VERIFICATION QUERIES
-- ============================================================================

-- Check record counts after load
CREATE VIEW v_data_quality_check AS
SELECT
    'dim_campaign' AS table_name,
    COUNT(*) AS record_count,
    'Active campaigns in database' AS description
FROM dim_campaign
UNION ALL
SELECT
    'fact_campaign_performance' AS table_name,
    COUNT(*) AS record_count,
    'Daily campaign performance records' AS description
FROM fact_campaign_performance
UNION ALL
SELECT
    'fact_shopify_sales' AS table_name,
    COUNT(*) AS record_count,
    'Sales transactions' AS description
FROM fact_shopify_sales
UNION ALL
SELECT
    'dim_date' AS table_name,
    COUNT(*) AS record_count,
    'Date dimension records' AS description
FROM dim_date;

-- ============================================================================
-- HELPER PROCEDURES (if using PostgreSQL)
-- ============================================================================

-- Function to populate date dimension (run once after setup)
-- For SQLite, execute the equivalent INSERT statements

-- Sample date dimension population (for 2024)
-- Run this query separately to populate dates:
-- INSERT INTO dim_date (date_id, date_value, day_of_week, day_of_month, week_of_year, month, quarter, year, is_weekend)
-- WITH RECURSIVE date_range AS (
--     SELECT DATE('2024-01-01') as date_val
--     UNION ALL
--     SELECT DATE(date_val, '+1 day')
--     FROM date_range
--     WHERE date_val < DATE('2024-12-31')
-- )
-- SELECT
--     ROWID,
--     date_val,
--     CAST(STRFTIME('%w', date_val) AS INTEGER),
--     CAST(STRFTIME('%d', date_val) AS INTEGER),
--     CAST(STRFTIME('%W', date_val) AS INTEGER),
--     CAST(STRFTIME('%m', date_val) AS INTEGER),
--     CAST((CAST(STRFTIME('%m', date_val) AS INTEGER) - 1) / 3 AS INTEGER) + 1,
--     CAST(STRFTIME('%Y', date_val) AS INTEGER),
--     CASE WHEN STRFTIME('%w', date_val) IN ('0', '6') THEN 1 ELSE 0 END
-- FROM date_range;
-- =====================================================
-- ADVANCED DIMENSION TABLES
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
-- PERFORMANCE INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_campaign_date
ON fact_campaign_performance(date);

CREATE INDEX IF NOT EXISTS idx_campaign_region
ON dim_campaign(target_region);

CREATE INDEX IF NOT EXISTS idx_campaign_funnel
ON dim_campaign(funnel_stage);

CREATE INDEX IF NOT EXISTS idx_campaign_roas
ON fact_campaign_performance(roas);

CREATE INDEX IF NOT EXISTS idx_campaign_spend
ON fact_campaign_performance(spend);

-- =====================================================
-- AI ANALYTICS VIEW
-- =====================================================

CREATE VIEW IF NOT EXISTS v_ai_creative_performance AS
SELECT
    c.creative_name,
    c.creative_format,
    AVG(f.roas) as avg_roas,
    AVG(f.ctr) as avg_ctr,
    AVG(f.cvr) as avg_cvr,
    SUM(f.spend) as total_spend,
    SUM(f.revenue) as total_revenue
FROM fact_campaign_performance f
LEFT JOIN dim_creative c
ON f.creative_id = c.creative_id
GROUP BY c.creative_name, c.creative_format;

CREATE VIEW IF NOT EXISTS v_ai_audience_performance AS
SELECT
    a.audience_type,
    a.interest_cluster,
    AVG(f.roas) as avg_roas,
    AVG(f.cpc) as avg_cpc,
    AVG(f.cvr) as avg_cvr,
    SUM(f.spend) as total_spend
FROM fact_campaign_performance f
LEFT JOIN dim_audience a
ON f.audience_id = a.audience_id
GROUP BY a.audience_type, a.interest_cluster;