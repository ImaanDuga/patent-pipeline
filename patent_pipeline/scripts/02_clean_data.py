"""
Script 2: Clean the raw data and export clean CSVs.
Outputs: data/clean/clean_patents.csv, clean_inventors.csv, clean_companies.csv
"""

import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from load_data_helper import load_all

RAW_DIR   = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')

def clean_patents(df):
    print("  Cleaning patents ...")
    print(f"    Columns found: {list(df.columns)}")
    cols = {
        'patent_id':    ['patent_id', 'id'],
        'title':        ['patent_title', 'title'],
        'abstract':     ['abstract'],
        'filing_date':  ['patent_date', 'filing_date', 'date'],
    }
    df = _select_cols(df, cols)
    df['filing_date'] = pd.to_datetime(df['filing_date'], errors='coerce')
    df['year'] = df['filing_date'].dt.year
    df.dropna(subset=['patent_id'], inplace=True)
    df.drop_duplicates(subset=['patent_id'], inplace=True)
    if 'title' in df.columns:
        df['title'] = df['title'].fillna('Unknown')
    else:
        df['title'] = 'Unknown'
    if 'abstract' in df.columns:
        df['abstract'] = df['abstract'].fillna('')
    else:
        df['abstract'] = ''
    print(f"    → {len(df):,} clean patents")
    return df

def clean_inventors(df, locations=None):
    print("  Cleaning inventors ...")
    cols = {
        'patent_id':    ['patent_id'],
        'inventor_id':  ['disambig_inventor_id', 'inventor_id', 'id'],
        'name':         ['disambig_inventor_name_first', 'inventor_name_first', 'name_first'],
        'last_name':    ['disambig_inventor_name_last',  'inventor_name_last',  'name_last'],
        'location_id':  ['location_id'],
        'country':      ['inventor_country', 'country', 'disambig_country'],
    }
    df = _select_cols(df, cols)
    # combine first + last into full name
    if 'last_name' in df.columns:
        df['name'] = (df['name'].fillna('') + ' ' + df['last_name'].fillna('')).str.strip()
        df.drop(columns=['last_name'], inplace=True)
    df.dropna(subset=['inventor_id'], inplace=True)

    # Join country from location file if available
    if locations is not None and 'location_id' in df.columns:
        loc = locations[['location_id', 'disambig_country']].dropna(subset=['disambig_country'])
        df = df.merge(loc, on='location_id', how='left')
        # use disambig_country if no direct country column
        if 'country' not in df.columns:
            df['country'] = df['disambig_country']
        else:
            df['country'] = df['country'].fillna(df['disambig_country'])
        df.drop(columns=['disambig_country'], errors='ignore', inplace=True)

    if 'location_id' in df.columns:
        df.drop(columns=['location_id'], inplace=True)

    df['country'] = df['country'].fillna('Unknown') if 'country' in df.columns else 'Unknown'
    print(f"    → {len(df):,} clean inventor records")
    return df

def clean_companies(df):
    print("  Cleaning companies ...")
    cols = {
        'patent_id':    ['patent_id'],
        'company_id':   ['disambig_assignee_id', 'assignee_id', 'id'],
        'name':         ['disambig_assignee_organization', 'assignee_organization', 'organization'],
    }
    df = _select_cols(df, cols)
    df.dropna(subset=['company_id'], inplace=True)
    df['name'] = df['name'].fillna('Unknown') if 'name' in df.columns else 'Unknown'
    print(f"    → {len(df):,} clean company records")
    return df

def _select_cols(df, col_map):
    """Pick the first matching column name for each target field."""
    rename = {}
    for target, candidates in col_map.items():
        for c in candidates:
            if c in df.columns:
                rename[c] = target
                break
    df = df.rename(columns=rename)
    keep = [t for t in col_map if t in df.columns]
    return df[keep].copy()

def main():
    print("=" * 50)
    print("STEP 2: Cleaning data")
    print("=" * 50)

    os.makedirs(CLEAN_DIR, exist_ok=True)

    raw = load_all(RAW_DIR)
    if raw is None:
        return

    patents        = clean_patents(raw['patents'])
    inventors_full = clean_inventors(raw['inventors'], locations=raw.get('locations'))
    companies_full = clean_companies(raw['assignees'])

    # --- Derive relationship tables from disambiguated files ---
    # patent_inventor: extract patent_id + inventor_id pairs
    if 'patent_id' in inventors_full.columns:
        pat_inv = inventors_full[['patent_id', 'inventor_id']].dropna()
        pat_inv.to_csv(os.path.join(CLEAN_DIR, 'patent_inventor.csv'), index=False)
        print(f"    → Derived {len(pat_inv):,} patent-inventor relationships")
    elif raw.get('pat_inv') is not None:
        raw['pat_inv'].to_csv(os.path.join(CLEAN_DIR, 'patent_inventor.csv'), index=False)
        print(f"    → Saved patent_inventor from raw file")

    # patent_company: extract patent_id + company_id pairs
    if 'patent_id' in companies_full.columns:
        pat_asgn = companies_full[['patent_id', 'company_id']].dropna()
        pat_asgn.to_csv(os.path.join(CLEAN_DIR, 'patent_assignee.csv'), index=False)
        print(f"    → Derived {len(pat_asgn):,} patent-company relationships")
    elif raw.get('pat_asgn') is not None:
        raw['pat_asgn'].to_csv(os.path.join(CLEAN_DIR, 'patent_assignee.csv'), index=False)
        print(f"    → Saved patent_assignee from raw file")

    # Deduplicate entity tables after extracting relationships
    inventors = inventors_full.drop(columns=['patent_id'], errors='ignore').drop_duplicates(subset=['inventor_id'])
    companies = companies_full.drop(columns=['patent_id'], errors='ignore').drop_duplicates(subset=['company_id'])

    patents.to_csv(os.path.join(CLEAN_DIR, 'clean_patents.csv'),     index=False)
    inventors.to_csv(os.path.join(CLEAN_DIR, 'clean_inventors.csv'), index=False)
    companies.to_csv(os.path.join(CLEAN_DIR, 'clean_companies.csv'), index=False)

    print(f"    → {len(inventors):,} unique inventors")
    print(f"    → {len(companies):,} unique companies")
    print("\n[OK] Clean files saved to data/clean/")

if __name__ == '__main__':
    main()
