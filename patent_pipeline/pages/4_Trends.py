import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Patent Trends", page_icon="📈", layout="wide")

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
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def _find_db():
    candidates = [
        os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db'),
        os.path.join(os.path.dirname(__file__), 'patent_pipeline.db'),
        os.path.join(os.getcwd(), 'patent_pipeline', 'patent_pipeline.db'),
        os.path.join(os.getcwd(), 'patent_pipeline.db'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]
DB_PATH = _find_db()

import sys
sys.path.insert(0, os.path.dirname(__file__))
from navbar import render_navbar

@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def get_trends():
    return pd.read_sql_query("""
        SELECT year, COUNT(*) AS patent_count
        FROM patents WHERE year IS NOT NULL
        GROUP BY year ORDER BY year
    """, get_conn())

with st.sidebar:
    st.markdown("## 🔬 Patent Intel")
    st.markdown("---")
    if st.button("🏠 Overview", width='stretch'):
        st.switch_page("dashboard.py")
    if st.button("🏆 Top Inventors", width='stretch'):
        st.switch_page("pages/1_Top_Inventors.py")
    if st.button("🏢 Top Companies", width='stretch'):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", width='stretch'):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", width='stretch', type="primary"):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", width='stretch'):
        st.switch_page("pages/5_Search.py")

render_navbar(active="trends")

st.markdown("""
<div class="page-header">
    <h2>📈 Patent Trends Over Time</h2>
    <p>Annual patent filing counts showing innovation activity over the years</p>
</div>
""", unsafe_allow_html=True)

df = get_trends()

if df.empty:
    st.warning("No trend data available.")
else:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['patent_count'],
        mode='lines+markers', name='Patents',
        line=dict(color='#1565c0', width=3),
        marker=dict(size=8, color='#1565c0', line=dict(color='white', width=2)),
        fill='tozeroy', fillcolor='rgba(21,101,192,0.08)',
        hovertemplate='<b>Year: %{x}</b><br>Patents: %{y:,}<extra></extra>'
    ))
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter, sans-serif', color='#334155'),
        title=dict(text='Patent Filings Over Time', font=dict(size=15, color='#0d2b5e')),
        xaxis=dict(title='Year', gridcolor='#f1f5f9', showgrid=True),
        yaxis=dict(title='Number of Patents', gridcolor='#f1f5f9', showgrid=True),
        hovermode='x unified', height=450,
        margin=dict(t=60, b=40, l=60, r=20),
        hoverlabel=dict(bgcolor='#0d2b5e', font_color='white')
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Peak Year", int(df.loc[df['patent_count'].idxmax(), 'year']))
    with col2:
        st.metric("Peak Count", f"{int(df['patent_count'].max()):,}")
    with col3:
        st.metric("Years Covered", int(df['year'].nunique()))

    st.markdown("---")
    st.markdown("#### 📋 Full Data Table")
    st.dataframe(
        df.rename(columns={'year': 'Year', 'patent_count': 'Patents'}),
        width='stretch', hide_index=True
    )
