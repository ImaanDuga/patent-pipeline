"""
Script 4: Run all 7 required SQL queries against the database.
Prints results to console and returns dataframes for use in reports.
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')

QUERIES = {
    'Q1_top_inventors': """
        SELECT i.name, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        GROUP BY i.inventor_id, i.name
        ORDER BY patent_count DESC
        LIMIT 20;
    """,

    'Q2_top_companies': """
        SELECT c.name, COUNT(pc.patent_id) AS patent_count
        FROM companies c
        JOIN patent_company pc ON c.company_id = pc.company_id
        GROUP BY c.company_id, c.name
        ORDER BY patent_count DESC
        LIMIT 20;
    """,

    'Q3_top_countries': """
        SELECT i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        WHERE i.country != 'Unknown'
        GROUP BY i.country
        ORDER BY patent_count DESC
        LIMIT 20;
    """,

    'Q4_trends_over_time': """
        SELECT year, COUNT(*) AS patent_count
        FROM patents
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year;
    """,

    'Q5_join_query': """
        SELECT p.patent_id, p.title, p.year,
               i.name  AS inventor_name,  i.country,
               c.name  AS company_name
        FROM patents p
        LEFT JOIN patent_inventor pi ON p.patent_id = pi.patent_id
        LEFT JOIN inventors i        ON pi.inventor_id = i.inventor_id
        LEFT JOIN patent_company pc  ON p.patent_id = pc.patent_id
        LEFT JOIN companies c        ON pc.company_id = c.company_id
        LIMIT 1000;
    """,

    'Q6_cte_query': """
        WITH inventor_counts AS (
            SELECT i.inventor_id, i.name, i.country,
                   COUNT(pi.patent_id) AS patent_count
            FROM inventors i
            JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
            GROUP BY i.inventor_id, i.name, i.country
        ),
        top_inventors AS (
            SELECT * FROM inventor_counts
            WHERE patent_count >= 5
        )
        SELECT country, COUNT(*) AS prolific_inventors, SUM(patent_count) AS total_patents
        FROM top_inventors
        GROUP BY country
        ORDER BY total_patents DESC
        LIMIT 15;
    """,

    'Q7_ranking_query': """
        SELECT name, country, patent_count,
               RANK()       OVER (ORDER BY patent_count DESC) AS overall_rank,
               RANK()       OVER (PARTITION BY country ORDER BY patent_count DESC) AS country_rank,
               ROUND(100.0 * patent_count / SUM(patent_count) OVER (), 4) AS pct_share
        FROM (
            SELECT i.inventor_id, i.name, i.country,
                   COUNT(pi.patent_id) AS patent_count
            FROM inventors i
            JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
            GROUP BY i.inventor_id, i.name, i.country
        )
        ORDER BY overall_rank
        LIMIT 30;
    """,
}

def run_all():
    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found. Run 03_store_db.py first.")
        return {}

    conn = sqlite3.connect(DB_PATH)
    results = {}

    print("=" * 50)
    print("STEP 4: Running SQL Queries")
    print("=" * 50)

    for name, sql in QUERIES.items():
        print(f"\n--- {name} ---")
        try:
            df = pd.read_sql_query(sql, conn)
            results[name] = df
            print(df.to_string(index=False))
        except Exception as e:
            print(f"  [ERROR] {e}")
            results[name] = pd.DataFrame()

    conn.close()
    return results

if __name__ == '__main__':
    run_all()
