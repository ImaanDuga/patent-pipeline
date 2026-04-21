"""
Script 3: Load clean CSVs into a SQLite database.
Creates patent_pipeline.db with all required tables.
"""

import pandas as pd
import sqlite3
import os

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')
DB_PATH   = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')

def load_clean(filename, required=True):
    path = os.path.join(CLEAN_DIR, filename)
    if not os.path.exists(path):
        if required:
            print(f"  [MISSING] {filename} — run 02_clean_data.py first")
        else:
            print(f"  [OPTIONAL] {filename} not found — skipping")
        return None
    return pd.read_csv(path, low_memory=False)

def main():
    print("=" * 50)
    print("STEP 3: Storing data in SQLite database")
    print("=" * 50)

    patents   = load_clean('clean_patents.csv')
    inventors = load_clean('clean_inventors.csv')
    companies = load_clean('clean_companies.csv')
    pat_inv   = load_clean('patent_inventor.csv', required=False)   # optional
    pat_asgn  = load_clean('patent_assignee.csv', required=False)   # optional

    if any(df is None for df in [patents, inventors, companies]):
        print("[ERROR] Missing core clean files. Run 02_clean_data.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    print(f"\n  Connected to: {DB_PATH}")

    # Apply schema first
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    print("  Schema applied.")

    # Insert data
    patents.to_sql('patents',   conn, if_exists='replace', index=False)
    print(f"  Inserted {len(patents):,} patents")

    inventors.to_sql('inventors', conn, if_exists='replace', index=False)
    print(f"  Inserted {len(inventors):,} inventors")

    companies.to_sql('companies', conn, if_exists='replace', index=False)
    print(f"  Inserted {len(companies):,} companies")

    if pat_inv is not None:
        # support both raw bridge file and derived relationship file
        rel_cols = [c for c in ['patent_id', 'inventor_id'] if c in pat_inv.columns]
        pat_inv[rel_cols].dropna().to_sql('patent_inventor', conn, if_exists='replace', index=False)
        print(f"  Inserted {len(pat_inv):,} patent-inventor relationships")
    else:
        print("  [SKIP] patent_inventor — file not found")

    if pat_asgn is not None:
        # support both raw bridge file (assignee_id) and derived file (company_id)
        if 'company_id' in pat_asgn.columns:
            rel_cols = [c for c in ['patent_id', 'company_id'] if c in pat_asgn.columns]
            pat_asgn[rel_cols].dropna().to_sql('patent_company', conn, if_exists='replace', index=False)
        else:
            rel_cols = [c for c in ['patent_id', 'assignee_id'] if c in pat_asgn.columns]
            pat_asgn_clean = pat_asgn[rel_cols].rename(columns={'assignee_id': 'company_id'})
            pat_asgn_clean.dropna().to_sql('patent_company', conn, if_exists='replace', index=False)
        print(f"  Inserted {len(pat_asgn):,} patent-company relationships")
    else:
        print("  [SKIP] patent_company — file not found")

    # Build combined relationships table (patent_id + inventor_id + company_id)
    if pat_inv is not None and pat_asgn is not None:
        print("\n  Building combined relationships table ...")
        inv_cols  = [c for c in ['patent_id', 'inventor_id'] if c in pat_inv.columns]
        asgn_cols = [c for c in ['patent_id', 'company_id']  if c in pat_asgn.columns]
        combined  = pat_inv[inv_cols].merge(pat_asgn[asgn_cols], on='patent_id', how='outer')
        combined.to_sql('patent_relationships', conn, if_exists='replace', index=False)
        print(f"  Inserted {len(combined):,} combined relationships")
    elif pat_inv is not None:
        inv_cols = [c for c in ['patent_id', 'inventor_id'] if c in pat_inv.columns]
        combined = pat_inv[inv_cols].copy()
        combined['company_id'] = None
        combined.to_sql('patent_relationships', conn, if_exists='replace', index=False)
        print(f"  Inserted {len(combined):,} combined relationships (no company data)")

    conn.commit()
    conn.close()
    print("\n[OK] Database ready: patent_pipeline.db")

if __name__ == '__main__':
    main()
