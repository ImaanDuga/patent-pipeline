"""
Patent Intelligence Dashboard - Main Landing Page
Run with: streamlit run patent_pipeline/dashboard.py
"""

import streamlit as st
import sqlite3
import os

st.set_page_config(
    page_title="Patent Intelligence Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Shared CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f4f8; }
    .hero-banner {
        background: linear-gradient(135deg, #0d2b5e 0%, #1a4a8a 60%, #1565c0 100%);
        padding: 2.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;
    }
    .hero-banner h1 { font-size: 2.4rem; font-weight: 700; margin: 0 0 0.4rem 0; }
    .hero-banner p  { font-size: 1.05rem; opacity: 0.85; margin: 0; }
    .hero-badge {
        display: inline-block; background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
        padding: 0.2rem 0.8rem; font-size: 0.78rem; margin-bottom: 0.8rem;
    }
    .metric-card {
        background: white; border-radius: 10px; padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07); border-left: 4px solid #1565c0;
    }
    .metric-label { font-size: 0.78rem; font-weight: 600; color: #64748b;
        text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.4rem; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #0d2b5e; line-height: 1; }
    .metric-icon  { font-size: 1.5rem; float: right; margin-top: -0.2rem; }
    .nav-card {
        background: white; border-radius: 10px; padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07); text-align: center;
        border-top: 4px solid #1565c0; transition: box-shadow 0.2s;
    }
    .nav-card h3 { color: #0d2b5e; margin: 0.5rem 0 0.3rem; font-size: 1.1rem; }
    .nav-card p  { color: #64748b; font-size: 0.88rem; margin: 0; }
    .nav-icon    { font-size: 2.2rem; }
    [data-testid="stSidebar"] { background: #0d2b5e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def _find_db():
    candidates = [
        os.path.join(os.path.dirname(__file__), 'patent_pipeline.db'),
        os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db'),
        os.path.join(os.getcwd(), 'patent_pipeline', 'patent_pipeline.db'),
        os.path.join(os.getcwd(), 'patent_pipeline.db'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]
DB_PATH = _find_db()

@st.cache_resource
def get_connection():
    if not os.path.exists(DB_PATH):
        st.error("Database not found. Run the pipeline first.")
        st.stop()
    return sqlite3.connect(DB_PATH, check_same_thread=False)

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
from navbar import render_navbar

def run_query(sql):
    conn = get_connection()
    return pd.read_sql_query(sql, conn)

render_navbar(active="overview")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🔬 USPTO PatentsView Data</div>
    <h1>Global Patent Intelligence</h1>
    <p>Explore innovation trends, top inventors, leading companies, and geographic patent distribution across 100,000 granted patents.</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics ────────────────────────────────────────────────────────────────────
stats = run_query("""
    SELECT
        (SELECT COUNT(*) FROM patents)   AS total_patents,
        (SELECT COUNT(*) FROM inventors) AS total_inventors,
        (SELECT COUNT(*) FROM companies) AS total_companies,
        (SELECT COUNT(DISTINCT country) FROM inventors WHERE country != 'Unknown') AS total_countries
""").iloc[0]

c1, c2, c3, c4 = st.columns(4)
for col, icon, label, value in [
    (c1, "📄", "Total Patents",   f"{int(stats['total_patents']):,}"),
    (c2, "👤", "Total Inventors", f"{int(stats['total_inventors']):,}"),
    (c3, "🏢", "Total Companies", f"{int(stats['total_companies']):,}"),
    (c4, "🌍", "Countries",       f"{int(stats['total_countries']):,}"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">{icon}</span>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── Navigation Cards ───────────────────────────────────────────────────────────
st.markdown("### 📂 Explore the Data")
st.markdown("Use the **sidebar** to navigate between sections, or click a card below.")
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<style>
    div[data-testid="column"] button {
        height: 120px !important;
        white-space: pre-wrap !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        color: #0d2b5e !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07) !important;
        border-top: 4px solid #1565c0 !important;
    }
    div[data-testid="column"] button:hover {
        box-shadow: 0 4px 16px rgba(21,101,192,0.2) !important;
        border-top: 4px solid #0d2b5e !important;
    }
</style>
""", unsafe_allow_html=True)

n1, n2, n3, n4, n5 = st.columns(5)
with n1:
    if st.button("🏆\n\nTop Inventors\n\nWho holds the most patents?", width='stretch'):
        st.switch_page("pages/1_Top_Inventors.py")
with n2:
    if st.button("🏢\n\nTop Companies\n\nLeading patent-holding firms", width='stretch'):
        st.switch_page("pages/2_Top_Companies.py")
with n3:
    if st.button("🌍\n\nTop Countries\n\nGeographic patent distribution", width='stretch'):
        st.switch_page("pages/3_Top_Countries.py")
with n4:
    if st.button("📈\n\nTrends\n\nPatent filings over time", width='stretch'):
        st.switch_page("pages/4_Trends.py")
with n5:
    if st.button("🔍\n\nSearch Patents\n\nFind patents by keyword", width='stretch'):
        st.switch_page("pages/5_Search.py")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Patent Intel")
    st.markdown("---")
    st.markdown("### Navigate")
    
    if st.button("🏠 Overview", width='stretch', type="primary"):
        st.switch_page("dashboard.py")
    if st.button("🏆 Top Inventors", width='stretch'):
        st.switch_page("pages/1_Top_Inventors.py")
    if st.button("🏢 Top Companies", width='stretch'):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", width='stretch'):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", width='stretch'):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", width='stretch'):
        st.switch_page("pages/5_Search.py")
    
    st.markdown("---")
    st.markdown("**Data Source**")
    st.markdown("USPTO PatentsView\n\n100,000 granted patents")
    st.markdown("---")
    st.markdown("<small style='opacity:0.6'>Global Patent Intelligence<br>Cloud Computing Project</small>",
                unsafe_allow_html=True)
