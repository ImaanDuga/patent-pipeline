"""
Shared helper used by other scripts to load raw TSV files.
The relationship files (pat_inv, pat_asgn) are optional — relationships
are derived from the disambiguated inventor/assignee files instead.
"""

import pandas as pd
import os

NROWS = 100_000  # set to None for full dataset

# Required files — pipeline cannot run without these
REQUIRED_FILES = {
    'patents':   'g_patent.tsv',
    'inventors': 'g_inventor_disambiguated.tsv',
    'assignees': 'g_assignee_disambiguated.tsv',
}

# Optional relationship files — used if present, derived otherwise
OPTIONAL_FILES = {
    'pat_inv':   'g_patent_inventor.tsv',
    'pat_asgn':  'g_patent_assignee.tsv',
    'locations': 'g_location_disambiguated.tsv',
}

def load_all(raw_dir, nrows=NROWS):
    result = {}
    all_required_ok = True

    # Load required files
    for key, fname in REQUIRED_FILES.items():
        path = os.path.join(raw_dir, fname)
        if not os.path.exists(path):
            print(f"  [MISSING] {fname}  ← required")
            all_required_ok = False
            result[key] = None
        else:
            result[key] = pd.read_csv(path, sep='\t', low_memory=False, nrows=nrows)
            print(f"  Loaded {fname}: {len(result[key]):,} rows")

    if not all_required_ok:
        print("\n[ERROR] Required files are missing. Download from:")
        print("  https://www.uspto.gov/ip-policy/economic-research/patentsview")
        return None

    # Load optional relationship files (won't abort if missing)
    for key, fname in OPTIONAL_FILES.items():
        path = os.path.join(raw_dir, fname)
        if not os.path.exists(path):
            print(f"  [OPTIONAL] {fname} not found — will derive relationships from disambiguated files")
            result[key] = None
        else:
            result[key] = pd.read_csv(path, sep='\t', low_memory=False, nrows=nrows)
            print(f"  Loaded {fname}: {len(result[key]):,} rows")

    return result
