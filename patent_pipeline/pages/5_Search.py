import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Search Patents", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f4f8; }
    .page-header {
        background: linear-gradient(135deg, #0d2b5e, #1565c0);
        color: white; padding: 1.5rem 2rem; border-radius: 10px; margin-bottom: 1.5rem;
    }
    .page-header h2 { margin: 0; font-size: 1.6rem; }
    .page-header p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.95rem; }
    [data-testid="stSidebar"] { background: #0d2b5e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stTextInput input {
        border-radius: 8px; border: 1.5px solid #cbd5e1;
        padding: 0.6rem 1rem; font-size: 1rem;
    }
    .stTextInput input:focus {
        border-color: #1565c0;
        box-shadow: 0 0 0 3px rgba(21,101,192,0.15);
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')

import sys
sys.path.insert(0, os.path.dirname(__file__))
from navbar import render_navbar

@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def search_patents(query):
    safe = query.replace("'", "''")
    return pd.read_sql_query(f"""
        SELECT p.patent_id, p.title, p.year,
               i.name AS inventor, i.country,
               c.name AS company
        FROM patents p
        LEFT JOIN patent_inventor pi ON p.patent_id = pi.patent_id
        LEFT JOIN inventors i        ON pi.inventor_id = i.inventor_id
        LEFT JOIN patent_company pc  ON p.patent_id = pc.patent_id
        LEFT JOIN companies c        ON pc.company_id = c.company_id
        WHERE p.title LIKE '%{safe}%'
        LIMIT 200
    """, get_conn())

with st.sidebar:
    st.markdown("## 🔬 Patent Intel")
    st.markdown("---")
    if st.button("🏠 Overview", use_container_width=True):
        st.switch_page("dashboard.py")
    if st.button("🏆 Top Inventors", use_container_width=True):
        st.switch_page("pages/1_Top_Inventors.py")
    if st.button("🏢 Top Companies", use_container_width=True):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", use_container_width=True):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", use_container_width=True):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Search.py")

render_navbar(active="search")

st.markdown("""
<div class="page-header">
    <h2>🔍 Search Patents</h2>
    <p>Search through 100,000 patent titles to find specific inventions</p>
</div>
""", unsafe_allow_html=True)

query = st.text_input("", placeholder="e.g., machine learning, battery, semiconductor, wireless, solar")

if query:
    with st.spinner("Searching..."):
        df = search_patents(query)

    if df.empty:
        st.info(f"No patents found matching **'{query}'**")
    else:
        st.success(f"Found **{len(df)}** results for **'{query}'**")
        st.dataframe(
            df.rename(columns={
                'patent_id': 'Patent ID', 'title': 'Title',
                'year': 'Year', 'inventor': 'Inventor',
                'country': 'Country', 'company': 'Company'
            }),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Patent ID": st.column_config.TextColumn(width="small"),
                "Title":     st.column_config.TextColumn(width="large"),
                "Year":      st.column_config.NumberColumn(width="small", format="%d"),
                "Inventor":  st.column_config.TextColumn(width="medium"),
                "Country":   st.column_config.TextColumn(width="small"),
                "Company":   st.column_config.TextColumn(width="medium"),
            }
        )
else:
    st.markdown("""
    #### 💡 Try searching for:
    - `machine learning` — AI and ML patents
    - `battery` — Energy storage innovations
    - `semiconductor` — Chip and electronics patents
    - `wireless` — Communication technology
    - `solar` — Renewable energy patents
    - `cancer` — Medical/biotech patents
    """)
