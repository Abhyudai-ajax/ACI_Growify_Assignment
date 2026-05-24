-- =====================================================
-- POPULATE ADVANCED METRICS
-- =====================================================

UPDATE fact_campaign_performance
SET revenue = conversions * 2500
WHERE revenue IS NULL;

UPDATE fact_campaign_performance
SET roas = ROUND(revenue / NULLIF(spend, 0), 2)
WHERE roas IS NULL;

UPDATE fact_campaign_performance
SET cvr = ROUND((conversions * 100.0) / NULLIF(clicks, 0), 2)
WHERE cvr IS NULL;

-- =====================================================
-- SAMPLE CREATIVE IDS
-- =====================================================

UPDATE fact_campaign_performance
SET creative_id =
CASE
    WHEN campaign_id % 3 = 0 THEN 1
    WHEN campaign_id % 3 = 1 THEN 2
    ELSE 3
END;

-- =====================================================
-- SAMPLE AUDIENCE IDS
-- =====================================================

UPDATE fact_campaign_performance
SET audience_id =
CASE
    WHEN campaign_id % 4 = 0 THEN 1
    WHEN campaign_id % 4 = 1 THEN 2
    WHEN campaign_id % 4 = 2 THEN 3
    ELSE 4
END;