"""
Script 6: Generate data visualizations from the patent database.
Outputs 4 charts to the output/charts/ directory:
  1. Top 10 Inventors (bar chart)
  2. Top 10 Companies (bar chart)
  3. Top 10 Countries (bar chart)
  4. Patents Over Time (line chart)
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

DB_PATH    = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'charts')

# ── Style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#f9f9f9',
    'axes.facecolor':   '#f9f9f9',
    'axes.edgecolor':   '#cccccc',
    'axes.grid':        True,
    'grid.color':       '#e0e0e0',
    'grid.linestyle':   '--',
    'font.family':      'sans-serif',
    'font.size':        11,
})

COLORS = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0',
          '#00BCD4', '#FF5722', '#607D8B', '#8BC34A', '#FFC107']


def get_data(conn, sql):
    return pd.read_sql_query(sql, conn)


def chart_top_inventors(conn, out_dir):
    df = get_data(conn, """
        SELECT i.name, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        GROUP BY i.inventor_id, i.name
        ORDER BY patent_count DESC
        LIMIT 10
    """)
    if df.empty:
        print("  [SKIP] No inventor data")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df['name'][::-1], df['patent_count'][::-1], color=COLORS)
    ax.set_xlabel('Number of Patents')
    ax.set_title('Top 10 Inventors by Patent Count', fontsize=14, fontweight='bold', pad=15)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{int(width)}', va='center', fontsize=10)

    plt.tight_layout()
    path = os.path.join(out_dir, 'top_inventors.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: charts/top_inventors.png")


def chart_top_companies(conn, out_dir):
    df = get_data(conn, """
        SELECT c.name, COUNT(pc.patent_id) AS patent_count
        FROM companies c
        JOIN patent_company pc ON c.company_id = pc.company_id
        GROUP BY c.company_id, c.name
        ORDER BY patent_count DESC
        LIMIT 10
    """)
    if df.empty:
        print("  [SKIP] No company data")
        return

    # Shorten long names
    df['short_name'] = df['name'].apply(lambda x: x[:35] + '…' if len(x) > 35 else x)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df['short_name'][::-1], df['patent_count'][::-1], color=COLORS)
    ax.set_xlabel('Number of Patents')
    ax.set_title('Top 10 Companies by Patent Count', fontsize=14, fontweight='bold', pad=15)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 5, bar.get_y() + bar.get_height() / 2,
                f'{int(width):,}', va='center', fontsize=10)

    plt.tight_layout()
    path = os.path.join(out_dir, 'top_companies.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: charts/top_companies.png")


def chart_top_countries(conn, out_dir):
    df = get_data(conn, """
        SELECT i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        WHERE i.country != 'Unknown'
        GROUP BY i.country
        ORDER BY patent_count DESC
        LIMIT 10
    """)
    if df.empty:
        print("  [SKIP] No country data")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['country'], df['patent_count'], color=COLORS)
    ax.set_xlabel('Country')
    ax.set_ylabel('Number of Patents')
    ax.set_title('Top 10 Countries by Patent Count', fontsize=14, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 100,
                f'{int(height):,}', ha='center', fontsize=9)

    plt.tight_layout()
    path = os.path.join(out_dir, 'top_countries.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: charts/top_countries.png")


def chart_trends(conn, out_dir):
    df = get_data(conn, """
        SELECT year, COUNT(*) AS patent_count
        FROM patents
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year
    """)
    if df.empty:
        print("  [SKIP] No trend data")
        return

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df['year'], df['patent_count'], color='#2196F3',
            linewidth=2.5, marker='o', markersize=5)
    ax.fill_between(df['year'], df['patent_count'], alpha=0.15, color='#2196F3')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Patents')
    ax.set_title('Patent Filings Over Time', fontsize=14, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.tight_layout()
    path = os.path.join(out_dir, 'patents_over_time.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: charts/patents_over_time.png")


def main():
    print("=" * 50)
    print("STEP 6: Generating Visualizations")
    print("=" * 50)

    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found. Run 03_store_db.py first.")
        return

    os.makedirs(CHARTS_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    chart_top_inventors(conn, CHARTS_DIR)
    chart_top_companies(conn, CHARTS_DIR)
    chart_top_countries(conn, CHARTS_DIR)
    chart_trends(conn, CHARTS_DIR)

    conn.close()
    print(f"\n[OK] All charts saved to output/charts/")


if __name__ == '__main__':
    main()
