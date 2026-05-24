# Power BI Dashboard Setup Guide

**Growify Digital - Complete Implementation Guide**

---

## 🎯 Overview

You'll create a **3-page professional marketing dashboard** that reads directly from your SQL database.

### Dashboard Pages
1. **Executive Summary** - KPIs and trends
2. **Channel Breakdown** - Platform and regional analysis
3. **Audience Insights** - Conversion analysis and drill-through

---

## 📋 Step 1: Connect to SQL Database

### In Power BI Desktop:

1. **File → New**
2. **Get Data → SQL Server**
   ```
   Server: localhost (or your database path)
   Database: cleaned_campaigns.db
   ```
3. **Select Tables:**
   - ☑ dim_campaign
   - ☑ dim_date
   - ☑ dim_product
   - ☑ fact_campaign_performance
   - ☑ fact_shopify_sales

4. **Click Load** (NOT Edit - we want live connection)

---

## 🔗 Step 2: Create Table Relationships

### In Model View:

Create these relationships (drag and drop):

| From | To | Type |
|------|-----|------|
| fact_campaign_performance[campaign_id] | dim_campaign[campaign_id] | One-to-Many |
| fact_campaign_performance[date_id] | dim_date[date_id] | One-to-Many |
| fact_shopify_sales[date_id] | dim_date[date_id] | One-to-Many |
| fact_shopify_sales[campaign_id] | dim_campaign[campaign_id] | One-to-Many |
| fact_shopify_sales[product_id] | dim_product[product_id] | One-to-Many |

---

## 📐 Step 3: Create DAX Measures

### In Data View, right-click each table and add measures:

### Core Metrics

```dax
-- SPEND METRICS
Total Spend = SUM(fact_campaign_performance[spend])

-- PERFORMANCE METRICS
Total Impressions = SUM(fact_campaign_performance[impressions])
Total Clicks = SUM(fact_campaign_performance[clicks])
Total Conversions = SUM(fact_campaign_performance[conversions])

-- SALES METRICS
Total Revenue = SUM(fact_shopify_sales[net_revenue])
Total Transactions = COUNTROWS(fact_shopify_sales)
Average Order Value = DIVIDE([Total Revenue], [Total Transactions], 0)

-- RATE METRICS
Avg CTR = AVERAGEX(fact_campaign_performance, fact_campaign_performance[ctr])
Avg CPC = AVERAGEX(fact_campaign_performance, fact_campaign_performance[cpc])
Avg CPM = AVERAGEX(fact_campaign_performance, fact_campaign_performance[cpm])

-- BUSINESS METRICS
ROAS = DIVIDE([Total Revenue], [Total Spend], 0)
Conversion Rate = DIVIDE([Total Conversions], [Total Clicks], 0) * 100
ROI = DIVIDE(([Total Revenue] - [Total Spend]), [Total Spend], 0) * 100

-- MONTH-OVER-MONTH CHANGE
MoM Spend Change = 
VAR CurrentMonth = [Total Spend]
VAR PreviousMonth = CALCULATE([Total Spend], DATEADD(dim_date[date_value], -1, MONTH))
RETURN IFERROR(
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0) * 100,
    0
)

-- COUNTRY-WISE TOTAL
Revenue by Region = 
VAR RegionRevenue = [Total Revenue]
RETURN RegionRevenue

-- PERFORMANCE RATINGS
Campaign Quality = 
VAR ROAS = [ROAS]
VAR CTR = [Avg CTR]
RETURN 
    IF(ROAS >= 2.5, "⭐⭐⭐⭐⭐",
    IF(ROAS >= 2.0, "⭐⭐⭐⭐",
    IF(ROAS >= 1.5, "⭐⭐⭐",
    IF(ROAS >= 1.0, "⭐⭐",
    IF(ROAS >= 0.5, "⭐",
    "❌ Needs Improvement")))))
```

---

## 🖼️ Step 4: Page 1 - Executive Summary

### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  EXECUTIVE SUMMARY - Marketing Performance Overview         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Total Spend]      [Total Revenue]    [ROAS]    [Avg CTR] │
│   $456,200             $1,280,500       2.81x      2.4%    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Spend vs Revenue Trend (Line Chart)                         │
│ ┌──────────────────────────────────────────────────────┐   │
│ │                    /                                 │   │
│ │               /                                      │   │
│ │          /                                           │   │
│ │     /                                                │   │
│ └──────────────────────────────────────────────────────┘   │
│ Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep        │
├─────────────────────────────────────────────────────────────┤
│ Top 5 Campaigns                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Campaign Name      │ Spend  │ Revenue │ ROAS │ Status  │ │
│ ├──────────────────────────────────────────────────────┤ │
│ │ SpringSale2024     │ $65k   │ $195k   │ 3.0x │ Active  │ │
│ │ SummerPromo        │ $54k   │ $162k   │ 3.0x │ Active  │ │
│ │ FallCampaign       │ $48k   │ $120k   │ 2.5x │ Paused  │ │
│ │ WinterSpecial      │ $42k   │ $100k   │ 2.4x │ Active  │ │
│ │ BackToSchool       │ $35k   │ $79k    │ 2.3x │ Active  │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Slicers: [Date Range ▼]  [Platform ▼]  [Region ▼]         │
└─────────────────────────────────────────────────────────────┘
```

### Add These Visuals:

1. **KPI Cards** (Top Left)
   - Card 1: Total Spend → [Total Spend] measure
   - Card 2: Total Revenue → [Total Revenue] measure
   - Card 3: ROAS → [ROAS] measure
   - Card 4: Avg CTR → [Avg CTR] measure
   - Format as currency/percent with icons

2. **Spend vs Revenue Trend** (Center)
   - Type: Line Chart
   - X-Axis: dim_date[date_value]
   - Y-Axis: [Total Spend] and [Total Revenue]
   - Trend line enabled
   - Data labels on

3. **Top 5 Campaigns Table** (Bottom)
   - Columns:
     - dim_campaign[campaign_name]
     - [Total Spend]
     - [Total Revenue]
     - [ROAS]
     - dim_campaign[status]
   - Sort by [Total Spend] descending
   - Conditional formatting on ROAS

4. **Slicers** (Right side)
   - Date slicer: dim_date[date_value]
   - Platform slicer: dim_campaign[platform]
   - Region slicer: dim_campaign[region]
   - Layout: Vertical, Light theme

---

## 🖼️ Step 5: Page 2 - Channel Breakdown

### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  CHANNEL BREAKDOWN - Platform & Channel Performance        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Performance by Platform (Bar)    │ Channel Mix (Donut)      │
│ ┌──────────────────────────────┐ ┌──────────────────────┐  │
│ │ Facebook    $156K ███████    │ │   Search   ████ 35%  │  │
│ │ Google      $132K ██████     │ │   Social   ████ 40%  │  │
│ │ Instagram   $98K  █████      │ │   Display  ██ 20%    │  │
│ │ TikTok      $42K  ██         │ │   Other    █ 5%      │  │
│ └──────────────────────────────┘ └──────────────────────┘  │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Regional Performance Matrix (Heat Map)                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Region │ Facebook │ Google │ Instagram │ TikTok │ Total│ │
│ ├──────────────────────────────────────────────────────┤ │
│ │ UK     │  2.8x   │  2.1x  │   3.2x    │  2.5x  │ 2.9x │ │
│ │ US     │  3.1x   │  2.8x  │   3.5x    │  2.9x  │ 3.1x │ │
│ │ EU     │  2.5x   │  1.9x  │   2.8x    │  2.2x  │ 2.4x │ │
│ │ ASIA   │  2.2x   │  1.7x  │   2.5x    │  2.0x  │ 2.1x │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Add These Visuals:

1. **Platform Performance** (Top Left)
   - Type: Bar Chart (Horizontal)
   - Axis: dim_campaign[platform]
   - Values: [Total Spend]
   - Secondary Y-Axis: [ROAS]
   - Data labels on

2. **Channel Mix** (Top Right)
   - Type: Donut Chart
   - Legend: dim_campaign[channel]
   - Values: [Total Spend]
   - Percentage labels enabled
   - Top colors

3. **Regional Performance Matrix** (Bottom)
   - Type: Matrix/Table
   - Rows: dim_campaign[region]
   - Columns: dim_campaign[platform]
   - Values: [ROAS]
   - Conditional formatting (color scale, blue→red)

4. **Drill-through** (Configure on this page)
   - Set campaigns table to allow drill-through
   - Click campaign name → detail page

---

## 🖼️ Step 6: Page 3 - Audience Insights

### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  AUDIENCE INSIGHTS - Conversion & Segmentation Analysis    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Conversion Rate by Region      │ Spend vs Conversions       │
│ ┌──────────────────────────────┐ ┌──────────────────────┐  │
│ │ US      ████████ 4.2%        │ │          •  •        │  │
│ │ UK      ███████  3.8%        │ │     •  •      •      │  │
│ │ EU      ██████   3.2%        │ │  •  •              • │  │
│ │ ASIA    █████    2.9%        │ │•                    │  │
│ └──────────────────────────────┘ └──────────────────────┘  │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Product Performance by Category                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Category       │ Revenue  │ Transactions │ Avg Value  │ │
│ ├──────────────────────────────────────────────────────┤ │
│ │ Electronics    │ $450,200 │ 1,250       │ $360      │ │
│ │ Apparel        │ $385,300 │ 2,150       │ $179      │ │
│ │ Home & Garden  │ $250,100 │ 800         │ $313      │ │
│ │ Beauty         │ $195,000 │ 1,200       │ $163      │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Add These Visuals:

1. **Conversion Rate by Region** (Top Left)
   - Type: Horizontal Bar
   - Axis: dim_campaign[region]
   - Values: [Conversion Rate] (%)
   - Data labels on

2. **Spend vs Conversions Scatter** (Top Right)
   - Type: Scatter Chart
   - X-Axis: [Total Spend]
   - Y-Axis: [Total Conversions]
   - Legend: dim_campaign[platform]
   - Bubble size: [ROAS]
   - Trend line enabled

3. **Product Performance** (Bottom)
   - Type: Table
   - Columns:
     - dim_product[product_name]
     - [Total Revenue]
     - [Total Transactions]
     - [Average Order Value]
   - Sort by [Total Revenue] descending
   - Conditional formatting

4. **Cross-Page Slicer**
   - Add to top of page
   - Slicer type: Date + Campaign name
   - Apply to all pages

---

## 🎨 Step 7: Formatting & Styling

### Color Scheme
```
Primary Blue:    #0063B1
Success Green:   #107C10
Warning Orange:  #FF8C00
Danger Red:      #D13438
Neutral Gray:    #737373
```

### Format Numbers
- **Currency**: $#,##0
- **Percent**: 0.0%
- **Decimals**: 0.00
- **Large Numbers**: Use K/M (e.g., $450K)

### Best Practices
1. ✅ Use white backgrounds for clarity
2. ✅ Minimize color usage (3-4 colors max)
3. ✅ Add clear titles to each visual
4. ✅ Include axis labels
5. ✅ Use data labels sparingly
6. ✅ Align all visuals to grid

---

## 🔍 Step 8: Add Drill-Through

### Configure Drill-Through:
1. Right-click a campaign name in Top 5 Campaigns table
2. **Drill-through → Create new page**
3. Name it "Campaign Details"
4. Add visuals filtered to selected campaign:
   - Daily metrics trend
   - Channel performance within campaign
   - Conversion funnel
   - Product breakdown

### Fields for Drill-Through
- dim_campaign[campaign_name]
- dim_campaign[platform]
- dim_campaign[region]

---

## ✅ Final Checklist

- [ ] SQL connection active (no CSV imports)
- [ ] All relationships configured correctly
- [ ] All measures working (no error symbols)
- [ ] Page 1: 4 KPI cards + 2 charts
- [ ] Page 2: 3 visuals + heat map
- [ ] Page 3: 3 visuals + scatter plot
- [ ] Slicers on all pages
- [ ] Drill-through configured
- [ ] Numbers formatted correctly
- [ ] Color scheme applied
- [ ] Saved as .pbix

---

## 📤 Exporting to PDF

1. **File → Export**
2. Select **PDF**
3. Choose **All Pages**
4. Options:
   - ✅ Include all pages
   - ✅ Fit to page width
   - ✅ High resolution
5. Save as **dashboard_export.pdf**

---

## 🚀 Tips for Excellence

1. **Add Icons to KPI Cards**
   - Use Power BI icons library
   - Spend: $ icon
   - Revenue: 💰 icon
   - ROAS: 📈 icon

2. **Use Bookmarks for Navigation**
   - Create "Reset" bookmark
   - Add buttons to bookmark buttons

3. **Add Tooltips**
   - Right-click visual → Tooltip
   - Explain what metrics mean

4. **Use Conditional Formatting**
   - Green for ROAS > 2.0
   - Red for CPC > average
   - Orange for low CTR

5. **Performance Optimization**
   - Hide unused fields
   - Use aggregated tables for large data
   - Reduce date precision if possible

---

## 📚 Resources

- [Power BI Best Practices](https://docs.microsoft.com/en-us/power-bi/service-best-practices)
- [DAX Function Reference](https://dax.guide/)
- [Color Accessibility](https://www.microsoft.com/design/inclusive/)

---

**Dashboard Version: 1.0**
**Last Updated: 2024**