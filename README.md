====================================================
   GLOBAL PATENT INTELLIGENCE DATA PIPELINE
====================================================

LIVE DASHBOARD:
  https://h5c2sts64arf4hbkwrqhja.streamlit.app/

GITHUB REPOSITORY:
  https://github.com/ImaanDuga/patent-pipeline

====================================================
PROJECT OVERVIEW
====================================================

A complete data engineering pipeline that collects,
cleans, stores, and analyzes 100,000 real-world
patent records from the USPTO PatentsView database.

====================================================
SETUP & INSTALLATION
====================================================

1. Install dependencies:
   pip install pandas sqlalchemy requests tqdm matplotlib streamlit plotly

2. Download these 4 files from PatentsView:
   https://data.uspto.gov/bulkdata/datasets/pvgpatdis
   - g_patent.tsv
   - g_inventor_disambiguated.tsv
   - g_assignee_disambiguated.tsv
   - g_location_disambiguated.tsv

   Place them in: patent_pipeline/data/raw/

====================================================
HOW TO RUN THE PIPELINE
====================================================

Run scripts in order:

  python patent_pipeline/scripts/01_load_data.py
  python patent_pipeline/scripts/02_clean_data.py
  python patent_pipeline/scripts/03_store_db.py
  python patent_pipeline/scripts/04_queries.py
  python patent_pipeline/scripts/05_reports.py
  python patent_pipeline/scripts/06_visualize.py

====================================================
HOW TO RUN THE DASHBOARD
====================================================

  streamlit run patent_pipeline/dashboard.py

Then open: http://localhost:8501

====================================================
OUTPUT FILES
====================================================

  patent_pipeline/output/
  ├── top_inventors.csv
  ├── top_companies.csv
  ├── country_trends.csv
  ├── patent_report.json
  ├── console_report.txt
  └── charts/
      ├── top_inventors.png
      ├── top_companies.png
      ├── top_countries.png
      └── patents_over_time.png

====================================================
KEY RESULTS
====================================================

  Total Patents:    100,000
  Total Inventors:   92,442
  Total Companies:   32,077
  Countries:             40+

  Top Inventors:
    1. Shunpei Yamazaki (JP) - 36 patents
    2. Kia Silverbrook (AU)  - 23 patents
    3. Tao Luo (US)          - 16 patents

  Top Companies:
    1. Samsung Display       - 2,065 patents
    2. IBM                   - 1,788 patents
    3. Canon                 - 1,048 patents

  Top Countries:
    1. United States         - 48,135 patents
    2. Japan                 - 16,747 patents
    3. Germany               -  5,825 patents

====================================================
TECHNOLOGIES USED
====================================================

  - Python        (pipeline scripting)
  - pandas        (data cleaning)
  - SQLite        (database storage)
  - SQL           (analytical queries)
  - Matplotlib    (static charts)
  - Plotly        (interactive charts)
  - Streamlit     (web dashboard)
  - GitHub        (version control)

====================================================
