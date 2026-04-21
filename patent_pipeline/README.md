# Global Patent Intelligence Data Pipeline

A complete data engineering pipeline that collects, cleans, stores, and analyzes real-world patent data from the USPTO PatentsView database.

## 📊 Project Overview

This pipeline processes patent data to understand:
- New technologies and innovation trends
- Top inventors and their contributions
- Leading companies in patent filings
- Geographic distribution of patents

## 🗂️ Project Structure

```
patent_pipeline/
├── data/
│   ├── raw/          ← place downloaded .tsv files here
│   └── clean/        ← cleaned CSVs (auto-generated)
├── scripts/
│   ├── 01_load_data.py
│   ├── 02_clean_data.py
│   ├── 03_store_db.py
│   ├── 04_queries.py
│   ├── 05_reports.py
│   ├── load_data_helper.py
│   └── queries_runner.py
├── sql/
│   └── schema.sql
├── output/           ← CSV + JSON reports (auto-generated)
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies
```bash
pip install pandas sqlalchemy requests tqdm
```

### Download Data Files

Download these 4 files from [PatentsView Granted Patent Disambiguated Data](https://data.uspto.gov/bulkdata/datasets/pvgpatdis):

**Required:**
- `g_patent.tsv`
- `g_inventor_disambiguated.tsv`
- `g_assignee_disambiguated.tsv`
- `g_location_disambiguated.tsv`

Place them in `patent_pipeline/data/raw/`

## ▶️ How to Run

Run scripts in order:

```bash
python patent_pipeline/scripts/01_load_data.py
python patent_pipeline/scripts/02_clean_data.py
python patent_pipeline/scripts/03_store_db.py
python patent_pipeline/scripts/04_queries.py
python patent_pipeline/scripts/05_reports.py
```

## 📁 Database Schema

### Tables

**patents**
- patent_id (PK)
- title
- abstract
- filing_date
- year

**inventors**
- inventor_id (PK)
- name
- country

**companies**
- company_id (PK)
- name

**patent_inventor** (relationship)
- patent_id (FK)
- inventor_id (FK)

**patent_company** (relationship)
- patent_id (FK)
- company_id (FK)

**patent_relationships** (combined)
- patent_id (FK)
- inventor_id (FK)
- company_id (FK)

## 📈 SQL Queries

The pipeline runs 7 analytical queries:

1. **Q1: Top Inventors** — Who has the most patents?
2. **Q2: Top Companies** — Which companies own the most patents?
3. **Q3: Top Countries** — Which countries produce the most patents?
4. **Q4: Trends Over Time** — Patent counts by year
5. **Q5: JOIN Query** — Combines patents with inventors and companies
6. **Q6: CTE Query** — Uses WITH statement for complex analysis
7. **Q7: Ranking Query** — Ranks inventors using window functions

## 📄 Output Reports

### A. Console Report
Terminal output with summary statistics

### B. CSV Exports
- `output/top_inventors.csv`
- `output/top_companies.csv`
- `output/country_trends.csv`

### C. JSON Report
- `output/patent_report.json`

## 🛠️ Technologies Used

- **Python** — Data processing and pipeline orchestration
- **pandas** — Data cleaning and transformation
- **SQLite** — Relational database storage
- **SQL** — Complex analytical queries

## 📊 Sample Results

**Top 5 Inventors:**
1. Shunpei Yamazaki — 36 patents
2. Kia Silverbrook — 23 patents
3. Tao Luo — 16 patents

**Top 5 Companies:**
1. SAMSUNG DISPLAY CO., LTD. — 2,065 patents
2. IBM — 1,788 patents
3. CANON KABUSHIKI KAISHA — 1,048 patents

**Top 5 Countries:**
1. US — 48,135 patents
2. JP — 16,747 patents
3. DE — 5,825 patents

## 🔄 Reproducibility

This project is fully reproducible. Clone the repo, download the data files, install dependencies, and run the scripts in order to generate identical results.

## 📝 Notes

- The pipeline processes 100,000 rows by default (configurable via `NROWS` in `load_data_helper.py`)
- Set `NROWS = None` to process the full dataset
- Raw data files are excluded from Git (see `.gitignore`)
- The database file is regenerated each time you run the pipeline

## 👤 Author

Built as part of a Cloud Computing / Data Engineering course project.

## 📜 License

Data sourced from USPTO PatentsView (public domain).

