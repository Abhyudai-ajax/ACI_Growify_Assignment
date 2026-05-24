DELETE FROM fact_campaign_performance;

WITH campaign_data AS (

    SELECT
        ROW_NUMBER() OVER () as unique_date_id,

        d.campaign_id,

        CAST(COALESCE(c."Impressions", 0) AS INTEGER) as impressions,

        CAST(COALESCE(c."Clicks (all)", 0) AS INTEGER) as clicks,

        CAST(COALESCE(c."Purchases", 0) AS INTEGER) as conversions,

        CAST(COALESCE(c."Amount Spent (INR)", 0) AS REAL) as spend,

        ROUND(
            (COALESCE(c."Clicks (all)", 0) * 100.0) /
            NULLIF(COALESCE(c."Impressions", 0), 0),
            2
        ) as ctr,

        ROUND(
            COALESCE(c."Amount Spent (INR)", 0) /
            NULLIF(COALESCE(c."Clicks (all)", 0), 0),
            2
        ) as cpc,

        ROUND(
            (COALESCE(c."Amount Spent (INR)", 0) * 1000.0) /
            NULLIF(COALESCE(c."Impressions", 0), 0),
            2
        ) as cpm,

        CAST(
            COALESCE(c."Purchases Conversion Value (INR)", 0)
            AS REAL
        ) as revenue,

        ROUND(
            COALESCE(c."Purchases Conversion Value (INR)", 0) /
            NULLIF(COALESCE(c."Amount Spent (INR)", 0), 0),
            2
        ) as roas,

        ROUND(
            (COALESCE(c."Purchases", 0) * 100.0) /
            NULLIF(COALESCE(c."Clicks (all)", 0), 0),
            2
        ) as cvr,

        CASE
            WHEN d.campaign_id % 3 = 0 THEN 1
            WHEN d.campaign_id % 3 = 1 THEN 2
            ELSE 3
        END as creative_id,

        CASE
            WHEN d.campaign_id % 4 = 0 THEN 1
            WHEN d.campaign_id % 4 = 1 THEN 2
            WHEN d.campaign_id % 4 = 2 THEN 3
            ELSE 4
        END as audience_id

    FROM campaigns c

    JOIN dim_campaign d
    ON d.campaign_name = c."Campaign Name"
)

INSERT INTO fact_campaign_performance (
    campaign_id,
    date_id,
    impressions,
    clicks,
    conversions,
    spend,
    ctr,
    cpc,
    cpm,
    revenue,
    roas,
    cvr,
    creative_id,
    audience_id
)

SELECT
    campaign_id,
    unique_date_id,
    impressions,
    clicks,
    conversions,
    spend,
    ctr,
    cpc,
    cpm,
    revenue,
    roas,
    cvr,
    creative_id,
    audience_id

FROM campaign_data;