import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class GrowifyAI:

    def __init__(self):
        self.db_path = "data/database/cleaned_campaigns.db"

    def run_query(self, query):

        conn = sqlite3.connect(self.db_path)

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    # =====================================================
    # CREATIVE INTELLIGENCE
    # =====================================================

    def creative_intelligence(self):

        query = """
        SELECT
            dc.creative_name,
            dc.creative_format,
            ROUND(AVG(f.roas), 2) as avg_roas,
            ROUND(AVG(f.ctr), 2) as avg_ctr,
            ROUND(AVG(f.cvr), 2) as avg_cvr,
            ROUND(SUM(f.spend), 2) as total_spend,
            ROUND(SUM(f.revenue), 2) as total_revenue

        FROM fact_campaign_performance f

        JOIN dim_creative dc
        ON f.creative_id = dc.creative_id

        GROUP BY dc.creative_name, dc.creative_format

        ORDER BY avg_roas DESC
        """

        df = self.run_query(query)

        print("\n" + "=" * 70)
        print("🎨 CREATIVE INTELLIGENCE")
        print("=" * 70)

        print(df)

        top = df.iloc[0]

        print("\n🚀 RECOMMENDATION:")
        print(
            f"SCALE '{top['creative_name']}' "
            f"({top['creative_format']}) "
            f"because it has strongest ROAS."
        )

    # =====================================================
    # AUDIENCE INTELLIGENCE
    # =====================================================

    def audience_intelligence(self):

        query = """
        SELECT
            da.audience_type,
            da.geo_segment,
            da.customer_persona,

            ROUND(AVG(f.roas), 2) as avg_roas,
            ROUND(AVG(f.cvr), 2) as avg_cvr,
            ROUND(SUM(f.revenue), 2) as total_revenue

        FROM fact_campaign_performance f

        JOIN dim_audience da
        ON f.audience_id = da.audience_id

        GROUP BY
            da.audience_type,
            da.geo_segment,
            da.customer_persona

        ORDER BY avg_roas DESC
        """

        df = self.run_query(query)

        print("\n" + "=" * 70)
        print("🧠 AUDIENCE INTELLIGENCE")
        print("=" * 70)

        print(df)

        top = df.iloc[0]

        print("\n🚀 RECOMMENDATION:")
        print(
            f"INCREASE budget for "
            f"{top['geo_segment']} audience "
            f"targeting {top['customer_persona']}."
        )

    # =====================================================
    # FUNNEL LEAK DETECTION
    # =====================================================

    def funnel_leak_detection(self):

        query = """
        SELECT
            dc.campaign_name,

            ROUND(AVG(f.ctr), 2) as avg_ctr,
            ROUND(AVG(f.cvr), 2) as avg_cvr,
            ROUND(AVG(f.roas), 2) as avg_roas

        FROM fact_campaign_performance f

        JOIN dim_campaign dc
        ON f.campaign_id = dc.campaign_id

        GROUP BY dc.campaign_name

        HAVING avg_ctr > 2
        AND avg_cvr < 1

        ORDER BY avg_ctr DESC
        """

        df = self.run_query(query)

        print("\n" + "=" * 70)
        print("⚠️ FUNNEL LEAK DETECTION")
        print("=" * 70)

        print(df)

        if len(df) > 0:

            print("\n🚨 INSIGHT:")
            print(
                "High CTR but low conversion detected.\n"
                "Possible landing page mismatch or weak checkout flow."
            )

    # =====================================================
    # ACTION ENGINE
    # =====================================================

    def action_engine(self):

        query = """
        SELECT
            dc.campaign_name,

            ROUND(AVG(f.roas), 2) as avg_roas,
            ROUND(SUM(f.spend), 2) as total_spend,
            ROUND(SUM(f.revenue), 2) as total_revenue

        FROM fact_campaign_performance f

        JOIN dim_campaign dc
        ON f.campaign_id = dc.campaign_id

        GROUP BY dc.campaign_name

        ORDER BY avg_roas DESC
        """

        df = self.run_query(query)

        print("\n" + "=" * 70)
        print("🤖 ACTION RECOMMENDATION ENGINE")
        print("=" * 70)

        for _, row in df.iterrows():

            if row["avg_roas"] >= 3:

                print(
                    f"✅ SCALE → {row['campaign_name']} "
                    f"(ROAS: {row['avg_roas']})"
                )

            elif row["avg_roas"] < 1:

                print(
                    f"❌ PAUSE → {row['campaign_name']} "
                    f"(ROAS: {row['avg_roas']})"
                )

            else:

                print(
                    f"⚠️ OPTIMIZE → {row['campaign_name']} "
                    f"(ROAS: {row['avg_roas']})"
                )

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(self):

        query = """
        SELECT
            ROUND(SUM(spend), 2) as total_spend,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(roas), 2) as avg_roas,
            ROUND(AVG(ctr), 2) as avg_ctr,
            ROUND(AVG(cvr), 2) as avg_cvr

        FROM fact_campaign_performance
        """

        df = self.run_query(query)

        print("\n" + "=" * 70)
        print("📊 EXECUTIVE SUMMARY")
        print("=" * 70)

        print(df)

    # =====================================================
    # MENU
    # =====================================================

    def run(self):

        while True:

            print("\n" + "=" * 70)
            print("🚀 GROWIFY AI INTELLIGENCE PLATFORM")
            print("=" * 70)

            print("""
1. Executive Summary
2. Creative Intelligence
3. Audience Intelligence
4. Funnel Leak Detection
5. Action Recommendation Engine
6. Exit
""")

            choice = input("Choose option: ")

            if choice == "1":
                self.executive_summary()

            elif choice == "2":
                self.creative_intelligence()

            elif choice == "3":
                self.audience_intelligence()

            elif choice == "4":
                self.funnel_leak_detection()

            elif choice == "5":
                self.action_engine()

            elif choice == "6":
                print("Goodbye 👋")
                break

            else:
                print("Invalid option")


if __name__ == "__main__":

    app = GrowifyAI()

    app.run()