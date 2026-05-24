"""
Data Cleaning & Validation Pipeline
Growify Digital - Data Analyst + AI Developer Assignment
Purpose: Clean raw ad and sales data, detect errors, validate metrics, load to SQL
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
from pathlib import Path
import logging

def parse_campaign_structure(campaign_name):
    if pd.isna(campaign_name):
        return pd.Series([
            None, None, None, None, None, None
        ])

    parts = [p.strip() for p in str(campaign_name).split("|")]

    while len(parts) < 6:
        parts.append(None)

    return pd.Series([
        parts[0],  # brand_name
        parts[1],  # campaign_launch
        parts[2],  # funnel_stage
        parts[3],  # campaign_type
        parts[4],  # target_region
        parts[5],  # audience_segment
    ])
    
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = DATA_DIR / "cleaned"
REPORT_DIR = DATA_DIR / "reports"
DATABASE_DIR = DATA_DIR / "database"
LOG_DIR = BASE_DIR / "logs"

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)




class DataQualityReport:
    """Track all data quality issues found and fixed"""
    def __init__(self):
        self.issues = []
        self.fixes = []
        self.stats = {}
    
    def add_issue(self, issue_type, description, count, severity='medium'):
        self.issues.append({
            'type': issue_type,
            'description': description,
            'count': count,
            'severity': severity
        })
    
    def add_fix(self, fix_type, description, rows_affected):
        self.fixes.append({
            'type': fix_type,
            'description': description,
            'rows_affected': rows_affected
        })
    
    def generate_report(self):
        """Generate markdown quality report"""
        report = "# Data Quality Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## Issues Found\n\n"
        for issue in self.issues:
            report += f"- **{issue['type']}** (Severity: {issue['severity']})\n"
            report += f"  - Description: {issue['description']}\n"
            report += f"  - Count: {issue['count']}\n\n"
        
        report += "## Fixes Applied\n\n"
        for fix in self.fixes:
            report += f"- **{fix['type']}**: {fix['description']}\n"
            report += f"  - Rows affected: {fix['rows_affected']}\n\n"
        
        report += "## Statistics\n\n"
        for key, value in self.stats.items():
            report += f"- {key}: {value}\n"
        
        return report


class CampaignDataCleaner:
    """Clean and validate campaign CSV data"""
    
    def __init__(self, filepath, quality_report):
        self.filepath = filepath
        self.report = quality_report
        self.df = None
        self.original_count = 0
        self.cleaned_count = 0
    
    def load_data(self):
        """Load CSV with flexible parsing"""
        try:
            self.df = pd.read_csv(self.filepath, dtype_backend='numpy_nullable')
            self.original_count = len(self.df)
            logger.info(f"Loaded {self.original_count} rows from {self.filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to load {self.filepath}: {e}")
            return False
    
    def detect_duplicates(self):
        """Identify and remove duplicate rows"""
        # Check for complete duplicates
        duplicates_full = self.df.duplicated().sum()
        
        # Check for functional duplicates (same campaign, date, platform, channel)
        key_cols = ['campaign_id', 'campaign_name', 'date', 'platform', 'channel']
        key_cols = [col for col in key_cols if col in self.df.columns]
        
        if key_cols:
            duplicates_func = self.df.duplicated(subset=key_cols, keep='first').sum()
        else:
            duplicates_func = 0
        
        total_duplicates = max(duplicates_full, duplicates_func)
        
        if total_duplicates > 0:
            self.df = self.df.drop_duplicates(subset=key_cols if key_cols else None, keep='first')
            self.report.add_issue(
                'Duplicate Rows',
                f'Found duplicates based on {key_cols if key_cols else "all columns"}',
                total_duplicates,
                'high'
            )
            self.report.add_fix(
                'Remove Duplicates',
                f'Removed {total_duplicates} duplicate rows',
                total_duplicates
            )
            logger.info(f"Removed {total_duplicates} duplicate rows")
    
    def standardize_dates(self):
        """Standardize all date formats to YYYY-MM-DD"""
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        
        for col in date_columns:
            try:
                # Try multiple date formats
                self.df[col] = pd.to_datetime(
                    self.df[col],
                    format='mixed',
                    errors='coerce'
                ).dt.strftime('%Y-%m-%d')
                
                # Flag rows where conversion failed
                null_dates = self.df[col].isnull().sum()
                if null_dates > 0:
                    self.report.add_issue(
                        'Invalid Date Format',
                        f'Column {col} had unparseable dates',
                        null_dates,
                        'high'
                    )
                    logger.warning(f"{null_dates} unparseable dates in {col}")
                    # Drop rows with invalid dates
                    self.df = self.df.dropna(subset=[col])
            except Exception as e:
                logger.error(f"Failed to standardize {col}: {e}")
        
        # Validate date logic (start <= end)
        if 'start_date' in self.df.columns and 'end_date' in self.df.columns:
            invalid_dates = (self.df['start_date'] > self.df['end_date']).sum()
            if invalid_dates > 0:
                self.report.add_issue(
                    'Invalid Date Logic',
                    'start_date > end_date (campaign duration backwards)',
                    invalid_dates,
                    'high'
                )
                # Swap them
                mask = self.df['start_date'] > self.df['end_date']
                self.df.loc[mask, ['start_date', 'end_date']] = \
                    self.df.loc[mask, ['end_date', 'start_date']].values
                logger.info(f"Fixed {invalid_dates} reversed date pairs")
    
    def handle_missing_values(self):
        """Handle missing values with justified strategy"""
        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing > 0:
                if col in ['spend', 'clicks', 'impressions', 'conversions']:
                    # For numeric metrics, fill with 0 (no activity = 0 spend/clicks)
                    self.df[col].fillna(0, inplace=True)
                    self.report.add_issue(
                        'Missing Numeric Value',
                        f'{col}: filled missing values with 0',
                        missing,
                        'medium'
                    )
                elif col in ['platform', 'channel', 'status']:
                    # For categorical, fill with 'Unknown'
                    self.df[col].fillna('Unknown', inplace=True)
                    self.report.add_issue(
                        'Missing Categorical Value',
                        f'{col}: filled missing values with "Unknown"',
                        missing,
                        'medium'
                    )
                else:
                    # For others, drop the row
                    self.df = self.df.dropna(subset=[col])
                    self.report.add_issue(
                        'Missing Critical Value',
                        f'{col}: dropped {missing} rows with missing values',
                        missing,
                        'high'
                    )
                logger.info(f"Handled {missing} missing values in {col}")
    
    def recalculate_metrics(self):
        """Recalculate CTR, CPM, CPC, ROI from source columns"""
        issues_found = 0
        
        # CTR = (Clicks / Impressions) * 100
        if 'clicks' in self.df.columns and 'impressions' in self.df.columns and 'ctr' in self.df.columns:
            self.df['clicks'] = pd.to_numeric(self.df['clicks'], errors='coerce').fillna(0)
            self.df['impressions'] = pd.to_numeric(self.df['impressions'], errors='coerce').fillna(0)
            
            # Calculate correct CTR
            correct_ctr = np.where(
                self.df['impressions'] > 0,
                (self.df['clicks'] / self.df['impressions']) * 100,
                0
            )
            
            # Flag mismatches
            ctr_mismatch = (~np.isclose(self.df['ctr'], correct_ctr, rtol=0.01, equal_nan=True)).sum()
            if ctr_mismatch > 0:
                self.report.add_issue(
                    'Incorrect CTR Calculation',
                    'CTR does not match (clicks/impressions)*100',
                    ctr_mismatch,
                    'high'
                )
                issues_found += ctr_mismatch
            
            self.df['ctr'] = correct_ctr
        
        # CPC = Spend / Clicks
        if 'spend' in self.df.columns and 'clicks' in self.df.columns and 'cpc' in self.df.columns:
            self.df['spend'] = pd.to_numeric(self.df['spend'], errors='coerce').fillna(0)
            correct_cpc = np.where(
                self.df['clicks'] > 0,
                self.df['spend'] / self.df['clicks'],
                0
            )
            
            cpc_mismatch = (~np.isclose(self.df['cpc'], correct_cpc, rtol=0.01, equal_nan=True)).sum()
            if cpc_mismatch > 0:
                self.report.add_issue(
                    'Incorrect CPC Calculation',
                    'CPC does not match spend/clicks',
                    cpc_mismatch,
                    'high'
                )
                issues_found += cpc_mismatch
            
            self.df['cpc'] = correct_cpc
        
        # CPM = (Spend / Impressions) * 1000
        if 'spend' in self.df.columns and 'impressions' in self.df.columns:
            correct_cpm = np.where(
                self.df['impressions'] > 0,
                (self.df['spend'] / self.df['impressions']) * 1000,
                0
            )
            if 'cpm' in self.df.columns:
                cpm_mismatch = (~np.isclose(self.df['cpm'], correct_cpm, rtol=0.01, equal_nan=True)).sum()
                if cpm_mismatch > 0:
                    self.report.add_issue(
                        'Incorrect CPM Calculation',
                        'CPM does not match (spend/impressions)*1000',
                        cpm_mismatch,
                        'high'
                    )
                    issues_found += cpm_mismatch
            self.df['cpm'] = correct_cpm
        
        if issues_found > 0:
            self.report.add_fix(
                'Recalculate Metrics',
                'Recalculated CTR, CPC, CPM from source columns',
                issues_found
            )
            logger.info(f"Fixed {issues_found} metric calculation errors")
    
    def normalize_strings(self):
        """Normalize categorical columns"""
        string_cols = [col for col in self.df.columns if self.df[col].dtype == 'object']
        
        for col in string_cols:
            if col in ['platform', 'channel', 'region', 'status']:
                # Standardize: lowercase, strip whitespace, handle mixed case
                original = self.df[col].copy()
                self.df[col] = self.df[col].str.strip().str.lower()
                
                # Flag inconsistencies
                inconsistencies = (~(original.str.lower().str.strip() == original)).sum()
                if inconsistencies > 0:
                    self.report.add_issue(
                        'Inconsistent String Format',
                        f'{col}: mixed case or leading/trailing spaces',
                        inconsistencies,
                        'medium'
                    )
                    logger.info(f"Normalized {inconsistencies} values in {col}")
    
    def detect_outliers(self):
        """Detect and flag statistical outliers"""
        numeric_cols = ['spend', 'clicks', 'impressions', 'conversions', 'cpc', 'cpm']
        numeric_cols = [col for col in numeric_cols if col in self.df.columns]
        
        for col in numeric_cols:
            if len(self.df[col]) > 0:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                if outliers > 0:
                    self.report.add_issue(
                        'Statistical Outliers',
                        f'{col}: {outliers} outliers detected (flagged for review)',
                        outliers,
                        'low'
                    )
                    logger.info(f"Detected {outliers} outliers in {col}")
    
    def clean(self):
        """Execute full cleaning pipeline"""
        logger.info("=== Starting Campaign Data Cleaning ===")
        
        if not self.load_data():
            return False
        
        self.detect_duplicates()
        self.standardize_dates()
        self.handle_missing_values()
        self.normalize_strings()
        self.recalculate_metrics()
        self.detect_outliers()
        
        self.cleaned_count = len(self.df)
        rows_removed = self.original_count - self.cleaned_count
        
        self.report.stats['Original Rows'] = self.original_count
        self.report.stats['Cleaned Rows'] = self.cleaned_count
        self.report.stats['Rows Removed'] = rows_removed
        
        logger.info(f"=== Cleaning Complete: {self.original_count} → {self.cleaned_count} rows ===")
        return True
    
    def to_sql(self, db_path, table_name):
        """Load cleaned data to SQLite"""
        try:
            conn = sqlite3.connect(db_path)
            self.df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            logger.info(f"Loaded {len(self.df)} rows to {table_name} in {db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load to SQL: {e}")
            return False


class ShopifyDataCleaner:
    """Clean and validate Shopify sales data"""
    
    def __init__(self, filepath, quality_report):
        self.filepath = filepath
        self.report = quality_report
        self.df = None
        self.original_count = 0
        self.cleaned_count = 0
    
    def load_data(self):
        """Load CSV with flexible parsing"""
        try:
            self.df = pd.read_csv(self.filepath, dtype_backend='numpy_nullable')
            self.original_count = len(self.df)
            logger.info(f"Loaded {self.original_count} rows from {self.filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to load {self.filepath}: {e}")
            return False
    
    def detect_duplicates(self):
        """Remove duplicate orders/transactions"""
        key_cols = [col for col in ['order_id', 'transaction_id', 'date'] 
                   if col in self.df.columns]
        
        if key_cols:
            duplicates = self.df.duplicated(subset=key_cols, keep='first').sum()
            if duplicates > 0:
                self.df = self.df.drop_duplicates(subset=key_cols, keep='first')
                self.report.add_issue(
                    'Duplicate Orders',
                    f'Duplicate transactions/orders removed',
                    duplicates,
                    'high'
                )
                logger.info(f"Removed {duplicates} duplicate transactions")
    
    def standardize_dates(self):
        """Standardize date formats"""
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        
        for col in date_columns:
            try:
                self.df[col] = pd.to_datetime(
                    self.df[col],
                    format='mixed',
                    errors='coerce'
                ).dt.strftime('%Y-%m-%d')
                
                null_dates = self.df[col].isnull().sum()
                if null_dates > 0:
                    self.report.add_issue(
                        'Invalid Date',
                        f'{col}: unparseable dates',
                        null_dates,
                        'high'
                    )
                    self.df = self.df.dropna(subset=[col])
            except Exception as e:
                logger.error(f"Date standardization failed for {col}: {e}")
    
    def handle_missing_values(self):
        """Handle missing values in sales data"""
        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing > 0:
                if col in ['revenue', 'amount', 'quantity', 'discount']:
                    self.df[col].fillna(0, inplace=True)
                elif col in ['product_name', 'customer_name', 'region']:
                    self.df[col].fillna('Unknown', inplace=True)
                else:
                    self.df = self.df.dropna(subset=[col])
                
                if missing > 0:
                    self.report.add_issue(
                        'Missing Value',
                        f'{col}: {missing} missing values handled',
                        missing,
                        'medium'
                    )
    
    def normalize_strings(self):
        """Normalize categorical columns"""
        string_cols = [col for col in self.df.columns if self.df[col].dtype == 'object']
        
        for col in string_cols:
            if col in ['region', 'country', 'status', 'product_category']:
                original = self.df[col].copy()
                self.df[col] = self.df[col].str.strip().str.lower()
                
                inconsistencies = (~(original.str.lower().str.strip() == original)).sum()
                if inconsistencies > 0:
                    self.report.add_issue(
                        'String Normalization',
                        f'{col}: normalized case and spacing',
                        inconsistencies,
                        'low'
                    )
    
    def clean(self):
        """Execute cleaning pipeline"""
        logger.info("=== Starting Shopify Data Cleaning ===")
        
        if not self.load_data():
            return False
        
        self.detect_duplicates()
        self.standardize_dates()
        self.handle_missing_values()
        self.normalize_strings()
        
        self.cleaned_count = len(self.df)
        rows_removed = self.original_count - self.cleaned_count
        
        self.report.stats['Shopify Original Rows'] = self.original_count
        self.report.stats['Shopify Cleaned Rows'] = self.cleaned_count
        self.report.stats['Shopify Rows Removed'] = rows_removed
        
        logger.info(f"=== Cleaning Complete: {self.original_count} → {self.cleaned_count} rows ===")
        return True
    
    def to_sql(self, db_path, table_name):
        """Load to SQL"""
        try:
            conn = sqlite3.connect(db_path)
            self.df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            logger.info(f"Loaded {len(self.df)} rows to {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to load to SQL: {e}")
            return False


def main():
    """Execute full cleaning pipeline"""
    
    # Initialize quality report
    report = DataQualityReport()
    
    # Clean campaign data
    logger.info("\n" + "="*60)
    logger.info("CLEANING CAMPAIGN DATA")
    logger.info("="*60 + "\n")
    
    campaign_path = DATA_DIR / "campaigns_raw.csv"
    campaign_cleaner = CampaignDataCleaner(campaign_path, report)
    if campaign_cleaner.clean():
        campaign_cleaner.to_sql(DATABASE_DIR / "cleaned_campaigns.db","campaigns")
    
    # Clean Shopify data
    logger.info("\n" + "="*60)
    logger.info("CLEANING SHOPIFY DATA")
    logger.info("="*60 + "\n")
    
    shopify_path = DATA_DIR / "Shopify_Raw.csv"
    shopify_cleaner = ShopifyDataCleaner(shopify_path, report)
    if shopify_cleaner.clean():
        shopify_cleaner.to_sql(DATABASE_DIR / "cleaned_campaigns.db","shopify_sales")
    # Generate quality report
    quality_report_text = report.generate_report()
    with open(REPORT_DIR / "data_quality_report.md", 'w') as f:
        f.write(quality_report_text)
    
    logger.info("\n" + "="*60)
    logger.info("DATA QUALITY REPORT GENERATED")
    logger.info("="*60)
    logger.info(quality_report_text)


if __name__ == '__main__':
    try:
        logger.info("Starting pipeline execution...")
        main()
        logger.info("Pipeline completed successfully.")
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        print(f"ERROR: {e}")
def parse_campaign_structure(campaign_name):
    if pd.isna(campaign_name):
        return pd.Series([
            None, None, None, None, None, None
        ])

    parts = [p.strip() for p in str(campaign_name).split("|")]

    while len(parts) < 6:
        parts.append(None)

    return pd.Series([
        parts[0],
        parts[1],
        parts[2],
        parts[3],
        parts[4],
        parts[5],
    ])


