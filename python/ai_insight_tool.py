import sqlite3
import json
import os
from typing import List, Dict
import logging

try:
    import anthropic
except ImportError:
    print("Installing anthropic...")
    os.system("pip install anthropic")
    import anthropic

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class DatabaseConnector:

    def __init__(self, db_path="data/database/cleaned_campaigns.db"):
        self.db_path = db_path

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None

    def execute_query(self, query):
        try:
            conn = self.get_connection()

            if conn is None:
                return []

            cursor = conn.cursor()
            cursor.execute(query)

            results = [dict(row) for row in cursor.fetchall()]

            conn.close()

            return results

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []

    def validate_query(self, query):

        dangerous_keywords = [
            'DROP',
            'DELETE',
            'TRUNCATE',
            'ALTER',
            'PRAGMA'
        ]

        query_upper = query.upper()

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Dangerous keyword found: {keyword}"

        if not query_upper.strip().startswith("SELECT"):
            return False, "Only SELECT queries allowed"

        return True, ""


class AIInsightTool:

    def __init__(self):

        self.db = DatabaseConnector()

        api_key = os.getenv("ANTHROPIC_API_KEY")

        self.client = None

        if api_key:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                logger.error(f"Anthropic init failed: {e}")

        logger.info("AI Insight Tool initialized")

    def fallback_sql(self, question):

        q = question.lower()

        if "highest roas" in q:
            return """
            SELECT
                campaign_name,
                roi_percent,
                roas
            FROM v_campaign_roi
            ORDER BY roas DESC
            LIMIT 5;
            """

        elif "india" in q:
            return """
            SELECT
                region,
                total_spend,
                roas
            FROM v_powerbi_regional_matrix
            WHERE LOWER(region) LIKE '%india%'
            ORDER BY total_spend DESC;
            """

        elif "funnel stage" in q:
            return """
            SELECT
                platform,
                channel,
                avg_ctr,
                roas
            FROM v_powerbi_platform_channel
            ORDER BY roas DESC
            LIMIT 10;
            """

        elif "high cpc" in q:
            return """
            SELECT
                campaign_name,
                avg_cpc
            FROM v_campaign_performance_monthly
            ORDER BY avg_cpc DESC
            LIMIT 10;
            """

        else:
            return """
            SELECT
                campaign_name,
                total_spend,
                roas
            FROM v_campaign_roi
            LIMIT 5;
            """

    def process_question(self, question):

        logger.info(f"Processing question: {question}")

        sql_query = self.fallback_sql(question)

        is_valid, error_msg = self.db.validate_query(sql_query)

        if not is_valid:
            return f"Validation failed: {error_msg}"

        results = self.db.execute_query(sql_query)

        if not results:
            return "No data found."

        response = f"""
============================================================
QUERY RESULTS
============================================================

SQL:
{sql_query}

------------------------------------------------------------
DATA
------------------------------------------------------------

{json.dumps(results[:5], indent=2)}

============================================================
"""

        return response

    def interactive_mode(self):

        print("\n" + "=" * 70)
        print("🚀 GROWIFY AI INSIGHT TOOL")
        print("=" * 70)

        print("Ask marketing questions.")
        print("Type 'exit' to quit.\n")

        while True:

            question = input("\n📝 Your question: ").strip()

            if question.lower() == "exit":
                print("Goodbye! 👋")
                break

            if not question:
                continue

            try:
                response = self.process_question(question)
                print(response)

            except Exception as e:
                logger.error(f"Processing failed: {e}")
                print(f"Error: {e}")


def main():

    tool = AIInsightTool()
    tool.interactive_mode()


if __name__ == "__main__":
    main()