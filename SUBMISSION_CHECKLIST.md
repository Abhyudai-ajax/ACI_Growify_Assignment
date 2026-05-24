# 📦 SUBMISSION GUIDE - Complete Checklist

**Growify Digital - Data Analyst + AI Developer Assignment**

---

## 🎯 Overview

This guide ensures you submit **everything needed** to get full marks.

### Points Breakdown
- **Python Data Cleaning**: 20 pts
- **Airtable Task**: 10 pts
- **SQL Schema & Queries**: 20 pts
- **Power BI Dashboard**: 20 pts
- **AI Tool**: 30 pts
- **Pipeline Integrity**: 15 pts
- **Bonus (Optional)**: +20 pts
- **TOTAL**: 115 pts (100 required + 15 bonus)

---

## 📁 Final Project Structure

Submit your project in this exact structure:

```
growify-data-pipeline/
│
├── README.md                                 # Main documentation ⭐
├── requirements.txt                          # Python dependencies
├── AIRTABLE_TASK_1.md                       # Airtable instructions
├── POWER_BI_SETUP.md                        # Power BI guide
│
├── /python
│   ├── data_cleaner.py                      # Data cleaning script
│   ├── ai_insight_tool.py                   # AI Q&A tool
│   └── config.py                            # Configuration (API keys)
│
├── /sql
│   ├── schema.sql                           # Full schema creation
│   └── queries.sql                          # Example queries
│
├── /data
│   ├── campaigns_raw.csv                    # Input (provided)
│   ├── Shopify_Raw.csv                      # Input (provided)
│   ├── cleaned_campaigns.db                 # Output (created by script)
│   └── data_quality_report.md               # Output (created by script)
│
├── /powerbi
│   ├── dashboard.pbix                       # Power BI workbook
│   └── dashboard_export.pdf                 # PDF export (all 3 pages)
│
├── /airtable
│   ├── airtable_screenshot.png              # Grouped view screenshot
│   └── airtable_setup_notes.txt             # Setup documentation
│
└── .env.example                              # Example env variables
    (ANTHROPIC_API_KEY=your_key_here)
```

---

## ✅ Task-by-Task Submission Checklist

### TASK 1: Airtable Setup (10 pts)

- [ ] **airtable_screenshot.png** - Screenshot of grouped view
  - Shows all 3 columns: Name, Number, Lead Priority
  - Shows all 3 rows of data
  - Shows grouping by Lead Priority active
  - Image is clear and readable
  - Filename: `airtable_screenshot.png`

- [ ] **airtable_setup_notes.txt** - Documentation
  - Explains what was created
  - Lists the columns and their types
  - Lists sample data used
  - Explains the grouping logic

**Submission**: Include both files in `/airtable` folder

---

### TASK 2: Python Data Cleaning (20 pts)

**Requirements Checklist:**

- [ ] **data_cleaner.py** - The cleaning script
  - ✅ Loads both CSV files correctly
  - ✅ Detects **duplicate rows** (explains method)
  - ✅ Standardizes **date formats** to YYYY-MM-DD
  - ✅ Validates **date logic** (start ≤ end)
  - ✅ Handles **missing values** with documented strategy
  - ✅ **Recalculates CTR** (clicks/impressions*100)
  - ✅ **Recalculates CPC** (spend/clicks)
  - ✅ **Recalculates CPM** (spend/impressions*1000)
  - ✅ **Flags wrong metrics** (compares calculated vs original)
  - ✅ **Normalizes strings** (platform, channel, region, status)
  - ✅ Detects **outliers** (IQR method)
  - ✅ Writes **comprehensive logging**
  - ✅ Outputs to SQL database (creates cleaned_campaigns.db)

- [ ] **cleaned_campaigns.db** - Output SQLite database
  - Contains `campaigns` table ✅
  - Contains `shopify_sales` table ✅
  - No duplicates ✅
  - Clean dates ✅
  - Correct calculations ✅

- [ ] **data_quality_report.md** - Quality documentation
  - Lists all issues found ✅
  - Describes fix for each issue ✅
  - Shows counts (e.g., "23 duplicates removed") ✅
  - Documents strategy for missing values ✅
  - Professional markdown format ✅

**Grading Criteria:**
- Issue detection completeness (5 pts)
- Fix strategy quality (5 pts)
- Output quality (5 pts)
- Report clarity (5 pts)

**Submission**: Include all 3 items in root or `/python` folder

---

### TASK 3: SQL Schema & Queries (20 pts)

**Requirements Checklist:**

- [ ] **schema.sql** - Complete SQL schema
  - ✅ **Star schema design**:
    - Dimension tables: dim_campaign, dim_date, dim_product
    - Fact tables: fact_campaign_performance, fact_shopify_sales
  - ✅ **Proper data types** (TEXT, INTEGER, DECIMAL)
  - ✅ **Primary keys** on all tables
  - ✅ **Foreign keys** linking facts to dimensions
  - ✅ **Date dimension table** with:
    - date_value, year, month, quarter, week_of_year, day_of_week
  - ✅ **Indexes**:
    - idx_dim_campaign_platform
    - idx_dim_campaign_channel
    - idx_dim_campaign_region
    - idx_fact_campaign_date_range
    - idx_fact_sales_region
  - ✅ **Clear comments** explaining each table
  - ✅ **Professional naming** (consistent_snake_case)

- [ ] **queries.sql** - Query templates
  - ✅ Query for Power BI aggregation (by platform, channel, region, month)
  - ✅ Flexible query for AI tool (filters by date, platform, region, campaign)
  - ✅ 8+ example queries provided
  - ✅ Comments explaining each query's purpose

- [ ] **Database verification**
  - ✅ Schema loads without errors: `sqlite3 cleaned_campaigns.db < schema.sql`
  - ✅ Tables created successfully
  - ✅ Data loads correctly

**Grading Criteria:**
- Schema design (5 pts)
- Query correctness (5 pts)
- Index choices & rationale (5 pts)
- Code readability & comments (5 pts)

**Submission**: `/sql` folder with both files

---

### TASK 4: Power BI Dashboard (20 pts)

**Requirements Checklist:**

- [ ] **dashboard.pbix** - Power BI workbook
  - ✅ **Connected to SQL database** (NOT CSV files)
  - ✅ **Data model relationships** configured:
    - fact_campaign_performance → dim_campaign
    - fact_campaign_performance → dim_date
    - fact_shopify_sales → dim_date
    - fact_shopify_sales → dim_campaign
    - fact_shopify_sales → dim_product
  - ✅ **Date dimension** properly configured (year/month/quarter hierarchies)
  - ✅ **8+ DAX measures** created:
    1. Total Spend
    2. Total Sales / Revenue
    3. ROI Total / Conversions
    4. CTR %
    5. CPC
    6. ROAS
    7. Countrywise Performance
    8. MoM Spend Change
  - ✅ **Page 1: Executive Summary**
    - KPI cards (4): Total Spend, Revenue, ROAS, Avg CTR
    - Spend vs Conversions trend (line chart)
    - Top 5 campaigns (table)
  - ✅ **Page 2: Channel Breakdown**
    - Performance by platform (bar chart)
    - Channel mix (donut chart)
    - Region matrix (heat map)
  - ✅ **Page 3: Audience Insights**
    - Conversion rate by segment (bar)
    - Spend vs conversions (scatter)
    - Product performance table
  - ✅ **Cross-page slicer** (date range + campaign name)
  - ✅ **Drill-through** configured

- [ ] **dashboard_export.pdf** - PDF export
  - ✅ All 3 pages exported
  - ✅ High resolution
  - ✅ Professional formatting
  - ✅ Readable and complete

**Grading Criteria:**
- SQL connection used correctly (4 pts)
- Data model quality (4 pts)
- DAX measures (4 pts)
- Report layout & storytelling (4 pts)
- Visual appeal & professionalism (4 pts)

**Submission**: `/powerbi` folder with .pbix and PDF

---

### TASK 5: AI Insight Tool (30 pts)

**Requirements Checklist:**

- [ ] **ai_insight_tool.py** - Complete implementation
  - ✅ **Accepts natural language questions** (CLI or UI)
  - ✅ **Text-to-SQL generation** (uses LLM to create SQL)
  - ✅ **SQL validation** (safety checks, only SELECT)
  - ✅ **Database queries** (executes SQL)
  - ✅ **LLM analysis** (Claude generates insight)
  - ✅ **Results presentation** (clean formatting)
  - ✅ **Conversational memory** (follow-ups work)
  - ✅ **Error handling** (graceful failures)
  - ✅ **Logging** (records operations)

- [ ] **Handle these questions** (test these):
  1. ✅ "Which campaign had the worst CPC in March?"
  2. ✅ "Summarise UK region performance"
  3. ✅ "Show top 5 campaigns by ROI"
  4. ✅ "Compare search vs social performance"
  5. ✅ "What was total revenue last month?"

- [ ] **README.md** - Documentation
  - ✅ Setup instructions (3-5 steps)
  - ✅ Usage examples (10+ questions)
  - ✅ Design decisions explained
  - ✅ Example questions with expected outputs
  - ✅ Troubleshooting section

- [ ] **Feature completeness**
  - ✅ Text-to-SQL working
  - ✅ Conversational memory working
  - ✅ Error handling in place
  - ✅ Results formatted nicely

**Grading Criteria:**
- End-to-end functionality (8 pts)
- SQL-to-context approach quality (8 pts)
- Prompt design & engineering (8 pts)
- Code structure & readability (6 pts)

**Submission**: `/python` folder with script + `/` folder with README

---

### TASK 6: Pipeline Integrity & Communication (15 pts)

**Requirements Checklist:**

- [ ] **Full pipeline works end-to-end**
  - ✅ Raw CSV → Python cleaner ✓
  - ✅ Python output → SQL database ✓
  - ✅ SQL database → Power BI ✓
  - ✅ SQL database → AI tool ✓
  - No CSV imports in Power BI ✓

- [ ] **Clear documentation**
  - ✅ README.md (comprehensive main doc)
  - ✅ Code comments (Python, SQL)
  - ✅ DAX measure explanations
  - ✅ Prompt engineering notes
  - ✅ Architecture diagram (optional but great)

- [ ] **Consistent data flow**
  - ✅ Same data in Power BI as AI tool
  - ✅ Metrics match between tools
  - ✅ No data discrepancies

- [ ] **Professional presentation**
  - ✅ Clear folder structure
  - ✅ Consistent naming
  - ✅ No unnecessary files
  - ✅ Ready to submit

**Grading Criteria:**
- Pipeline cohesion (5 pts)
- README clarity (5 pts)
- Code documentation (5 pts)

**Submission**: Entire project folder

---

### BONUS: Optional Advanced Features (+20 pts)

Pick ONE to implement for bonus points:

#### Option 1: Text-to-SQL ⭐⭐ (Recommended)
- [ ] AI tool auto-generates SQL from questions
- [ ] No hard-coded query templates
- [ ] Works with varied question phrasing
- [ ] Validates generated SQL before execution
- **Points**: +20 pts

#### Option 2: Power BI + AI Integration
- [ ] AI tool embedded in Power BI visual
- [ ] Single interface for both tools
- [ ] Questions can reference Power BI context
- **Points**: +15 pts

#### Option 3: Anomaly Detection
- [ ] Detects unusual spend/CPC
- [ ] Surfaces alerts in Power BI
- [ ] Dedicated alert page
- [ ] Statistical methods explained
- **Points**: +15 pts

#### Option 4: Budget Optimizer
- [ ] Takes total budget input
- [ ] Recommends channel allocation
- [ ] Based on historical ROAS
- [ ] Shows projected performance
- **Points**: +15 pts

**Note**: We grade one well-executed bonus higher than three half-finished ones.

---

## 📹 Video Submission (MANDATORY - 5-10 minutes)

You MUST submit a video explaining your solution.

### What to Cover:

1. **Introduction** (30 sec)
   - "Hi, I'm building a data pipeline for Growify Digital"
   - Overview of what the project does

2. **Data Cleaning** (1-2 min)
   - Show the data_cleaner.py running
   - Demo the quality report
   - Explain 3-4 issues found and fixed
   - Show the database created

3. **SQL Architecture** (1 min)
   - Explain star schema design
   - Show the dimension/fact tables
   - Explain why you chose this design

4. **Power BI Dashboard** (2 min)
   - Walk through each page
   - Show the SQL connection
   - Explain 2-3 key measures
   - Show interactivity (slicing/filtering)

5. **AI Tool Demo** (2 min)
   - Ask 3 example questions
   - Show how it generates SQL
   - Show conversational memory in action
   - Explain design decisions

6. **Pipeline Overview** (1 min)
   - Show the flow: CSV → Python → SQL → BI & AI
   - Emphasize single source of truth (SQL)
   - Highlight key design decisions

7. **Conclusion** (30 sec)
   - Summary of what was built
   - Key learnings
   - Thank you

### Recording Tips:
- ✅ Use screen recording (OBS, Loom, ScreenFlow)
- ✅ Speak clearly and at normal pace
- ✅ High resolution (1080p or 4K)
- ✅ Good audio quality
- ✅ Include captions/subtitles if possible
- ✅ Show code in IDE (syntax highlighting)
- ❌ Don't read from script word-for-word

### Submission Format:
- **File**: `video_explanation.mp4` (or YouTube link)
- **Hosting**: Upload to YouTube (unlisted) or include in ZIP
- **Duration**: 5-10 minutes

---

## 🎓 Final Submission Package

Create a GitHub repository or ZIP file with:

```
growify-data-pipeline-submission/
├── README.md                    # 📌 Start here
├── requirements.txt
├── video_explanation.mp4        # 🎥 Required
│
├── /python
│   ├── data_cleaner.py
│   ├── ai_insight_tool.py
│   └── __init__.py
│
├── /sql
│   ├── schema.sql
│   └── queries.sql
│
├── /data
│   ├── cleaned_campaigns.db
│   └── data_quality_report.md
│
├── /powerbi
│   ├── dashboard.pbix
│   └── dashboard_export.pdf
│
├── /airtable
│   ├── airtable_screenshot.png
│   └── airtable_setup_notes.txt
│
├── AIRTABLE_TASK_1.md
├── POWER_BI_SETUP.md
├── SUBMISSION_CHECKLIST.md
└── .env.example
```

---

## 🚀 Quick Verification Checklist (Before Submitting)

Run these checks:

```bash
# 1. Check Python syntax
python -m py_compile python/data_cleaner.py
python -m py_compile python/ai_insight_tool.py

# 2. Check SQL syntax
sqlite3 :memory: < sql/schema.sql

# 3. Check database exists
ls -la data/cleaned_campaigns.db

# 4. Check all required files exist
ls -la *.md
ls -la python/*
ls -la sql/*
ls -la data/*
ls -la powerbi/*
ls -la airtable/*

# 5. Test data cleaner
python python/data_cleaner.py
# Should create: cleaned_campaigns.db, data_quality_report.md

# 6. Test AI tool
python python/ai_insight_tool.py
# Should start interactive mode
```

---

## ✅ Final Submission Checklist

- [ ] All files in correct folder structure
- [ ] README.md complete and clear
- [ ] data_cleaner.py works without errors
- [ ] cleaned_campaigns.db created
- [ ] data_quality_report.md generated
- [ ] schema.sql loads correctly
- [ ] Power BI dashboard connects to SQL (not CSV)
- [ ] All 3 pages in Power BI dashboard
- [ ] PDF export of all pages
- [ ] AI tool runs and answers questions
- [ ] Airtable screenshot included
- [ ] Video explanation (5-10 min) included
- [ ] requirements.txt complete
- [ ] All code has comments
- [ ] No hardcoded API keys (use .env)
- [ ] Project is ready to deploy
- [ ] GitHub repo or ZIP created
- [ ] Deadline met (3-4 days)

---

## 📧 Submission Instructions

### Option 1: GitHub (Preferred)
1. Create private GitHub repo: `growify-data-pipeline`
2. Push all code and files
3. Add `.gitignore` (exclude: .env, *.db, __pycache__)
4. Submit repo link

### Option 2: ZIP File
1. Create folder: `growify-data-pipeline`
2. Add all files (structure as above)
3. Zip the folder
4. Submit: `growify-data-pipeline.zip`

### Both Should Include:
- ✅ All source code
- ✅ Output database
- ✅ Quality report
- ✅ Power BI workbook
- ✅ Video explanation
- ✅ Complete documentation

---

## 🎯 Grading Rubric Summary

| Component | Points | Status |
|-----------|--------|--------|
| Python - Data Cleaning | 20 | ☐ |
| Airtable Task | 10 | ☐ |
| SQL - Schema & Queries | 20 | ☐ |
| Power BI - Dashboard | 20 | ☐ |
| AI Tool - Code & Prompts | 30 | ☐ |
| Pipeline Integrity | 15 | ☐ |
| **TOTAL** | **115** | ☐ |
| Bonus (Optional) | +20 | ☐ |

---

## 🎓 What Evaluators Look For

> ⭐ **"We evaluate thinking as much as output."**

They'll assess:
1. **Completeness**: Did you handle all requirements?
2. **Quality**: Is the code production-ready?
3. **Clarity**: Can others understand your decisions?
4. **Professionalism**: Is it well-documented?
5. **Creativity**: Did you add thoughtful touches?
6. **End-to-End**: Does the whole pipeline work together?

### Pro Tips:
- ✅ Comment your SQL like you're writing documentation
- ✅ Explain DAX measure logic in Power BI
- ✅ Document prompt engineering decisions
- ✅ Show your reasoning in README
- ✅ Submit early to get feedback
- ✅ Test everything before submitting

---

## 📞 If You Get Stuck

1. **Data cleaning issues**: Check data_quality_report.md
2. **SQL errors**: Run queries in SQLite to debug
3. **Power BI connection**: Verify database path
4. **AI tool errors**: Check ANTHROPIC_API_KEY
5. **Python issues**: Check requirements.txt and install

---

## 🎉 You're Ready!

Follow this checklist, and you'll submit an **exceptional assignment** that showcases:
- Data engineering skills
- SQL expertise
- BI tool mastery
- AI/ML integration
- Professional communication

**Good luck! 🚀**

---

**Last Updated**: 2024
**Assignment Version**: 1.0