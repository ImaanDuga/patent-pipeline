"""
Script 5: Generate all 3 required report types.
  A. Console report (terminal output)
  B. CSV exports (top_inventors, top_companies, country_trends)
  C. JSON report
"""

import sqlite3
import pandas as pd
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from queries_runner import run_all

DB_PATH    = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

def get_total_patents(conn):
    return pd.read_sql_query("SELECT COUNT(*) AS total FROM patents;", conn).iloc[0]['total']

def console_report(results, total_patents):
    print("\n")
    print("=" * 52)
    print("           PATENT INTELLIGENCE REPORT")
    print("=" * 52)
    print(f"  Total Patents: {int(total_patents):,}")

    print("\n  Top 5 Inventors:")
    if 'Q1_top_inventors' in results and not results['Q1_top_inventors'].empty:
        for i, row in results['Q1_top_inventors'].head(5).iterrows():
            print(f"    {i+1}. {row['name']} — {int(row['patent_count'])} patents")

    print("\n  Top 5 Companies:")
    if 'Q2_top_companies' in results and not results['Q2_top_companies'].empty:
        for i, row in results['Q2_top_companies'].head(5).iterrows():
            print(f"    {i+1}. {row['name']} — {int(row['patent_count'])} patents")

    print("\n  Top 5 Countries:")
    if 'Q3_top_countries' in results and not results['Q3_top_countries'].empty:
        for i, row in results['Q3_top_countries'].head(5).iterrows():
            print(f"    {i+1}. {row['country']} — {int(row['patent_count'])} patents")

    print("\n  Patent Trends (last 5 years):")
    if 'Q4_trends_over_time' in results and not results['Q4_trends_over_time'].empty:
        for _, row in results['Q4_trends_over_time'].tail(5).iterrows():
            print(f"    {int(row['year'])}: {int(row['patent_count']):,} patents")

    print("=" * 52)

def csv_reports(results, output_dir):
    exports = {
        'top_inventors.csv':   ('Q1_top_inventors',    20),
        'top_companies.csv':   ('Q2_top_companies',    20),
        'country_trends.csv':  ('Q3_top_countries',    None),
    }
    for filename, (query_key, limit) in exports.items():
        df = results.get(query_key, pd.DataFrame())
        if not df.empty:
            out = df.head(limit) if limit else df
            path = os.path.join(output_dir, filename)
            out.to_csv(path, index=False)
            print(f"  Saved: {filename}")

def json_report(results, total_patents, output_dir):
    def safe_list(key, name_col, count_col, limit=10):
        df = results.get(key, pd.DataFrame())
        if df.empty:
            return []
        return [
            {name_col: row[name_col], count_col: int(row[count_col])}
            for _, row in df.head(limit).iterrows()
        ]

    report = {
        "total_patents": int(total_patents),
        "top_inventors": safe_list('Q1_top_inventors', 'name', 'patent_count'),
        "top_companies": safe_list('Q2_top_companies', 'name', 'patent_count'),
        "top_countries": safe_list('Q3_top_countries', 'country', 'patent_count'),
        "yearly_trends": safe_list('Q4_trends_over_time', 'year', 'patent_count', limit=50),
    }

    path = os.path.join(output_dir, 'patent_report.json')
    with open(path, 'w') as f:
        json.dump(report, f, indent=2, default=lambda o: int(o) if hasattr(o, 'item') else str(o))
    print(f"  Saved: patent_report.json")

def main():
    print("=" * 50)
    print("STEP 5: Generating Reports")
    print("=" * 50)

    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found. Run 03_store_db.py first.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = run_all()
    conn    = sqlite3.connect(DB_PATH)
    total   = get_total_patents(conn)
    conn.close()

    # A. Console report
    console_report(results, total)

    # B. CSV reports
    print("\n  Exporting CSVs ...")
    csv_reports(results, OUTPUT_DIR)

    # C. JSON report
    print("\n  Exporting JSON ...")
    json_report(results, total, OUTPUT_DIR)

    print("\n[OK] All reports saved to output/")

if __name__ == '__main__':
    main()
