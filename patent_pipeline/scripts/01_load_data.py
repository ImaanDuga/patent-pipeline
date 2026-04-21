"""
Script 1: Load raw patent data from TSV files.
Place downloaded files in data/raw/ before running.
Loads a sample (nrows) to keep things manageable — set nrows=None for full data.
"""

import pandas as pd
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
NROWS = 100_000  # change to None to load everything

FILES = {
    'patents':   'g_patent.tsv',
    'inventors': 'g_inventor_disambiguated.tsv',
    'assignees': 'g_assignee_disambiguated.tsv',
    'pat_inv':   'g_patent_inventor.tsv',
    'pat_asgn':  'g_patent_assignee.tsv',
}

def load_tsv(filename, nrows=NROWS):
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        print(f"  [MISSING] {filename} — place it in data/raw/")
        return None
    print(f"  Loading {filename} ...")
    df = pd.read_csv(path, sep='\t', low_memory=False, nrows=nrows)
    print(f"    → {len(df):,} rows, {df.shape[1]} columns")
    return df

def main():
    print("=" * 50)
    print("STEP 1: Loading raw data")
    print("=" * 50)

    os.makedirs(RAW_DIR, exist_ok=True)

    dataframes = {}
    for key, fname in FILES.items():
        dataframes[key] = load_tsv(fname)

    missing = [k for k, v in dataframes.items() if v is None]
    if missing:
        print(f"\n[WARNING] Missing files: {missing}")
        print("Download them from: https://data.uspto.gov/bulkdata/datasets/pvgpatdis")
    else:
        print("\n[OK] All files loaded successfully.")

    return dataframes

if __name__ == '__main__':
    main()
