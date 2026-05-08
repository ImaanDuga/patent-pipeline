====================================================
   GLOBAL PATENT INTELLIGENCE DATA PIPELINE
====================================================

LIVE DASHBOARD:
  https://h5c2sts64arf4hbkwrqhja.streamlit.app/

GITHUB REPOSITORY:
  https://github.com/ImaanDuga/patent-pipeline

====================================================
KEY RESULTS
====================================================

  Total Patents:    100,000
  Total Inventors:   92,442
  Total Companies:   32,077

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
HOW TO RUN
====================================================

  pip install pandas sqlalchemy requests tqdm matplotlib streamlit plotly

  python patent_pipeline/scripts/01_load_data.py
  python patent_pipeline/scripts/02_clean_data.py
  python patent_pipeline/scripts/03_store_db.py
  python patent_pipeline/scripts/04_queries.py
  python patent_pipeline/scripts/05_reports.py
  python patent_pipeline/scripts/06_visualize.py
  streamlit run patent_pipeline/dashboard.py

====================================================
