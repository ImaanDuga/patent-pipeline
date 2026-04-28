import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Top Companies", page_icon="🏢", layout="wide")

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

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'patent_pipeline.db')

import sys
sys.path.insert(0, os.path.dirname(__file__))
from navbar import render_navbar

@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def get_top_companies(limit):
    return pd.read_sql_query(f"""
        SELECT c.name, COUNT(pc.patent_id) AS patent_count
        FROM companies c
        JOIN patent_company pc ON c.company_id = pc.company_id
        GROUP BY c.company_id, c.name
        ORDER BY patent_count DESC
        LIMIT {limit}
    """, get_conn())

with st.sidebar:
    st.markdown("## 🔬 Patent Intel")
    st.markdown("---")
    if st.button("🏠 Overview", width='stretch'):
        st.switch_page("dashboard.py")
    if st.button("🏆 Top Inventors", width='stretch'):
        st.switch_page("pages/1_Top_Inventors.py")
    if st.button("🏢 Top Companies", width='stretch', type="primary"):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", width='stretch'):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", width='stretch'):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", width='stretch'):
        st.switch_page("pages/5_Search.py")

render_navbar(active="companies")

st.markdown("""
<div class="page-header">
    <h2>🏢 Top Companies</h2>
    <p>Companies ranked by total number of granted patents</p>
</div>
""", unsafe_allow_html=True)

limit = st.slider("Number of companies to display", 5, 50, 20)
df = get_top_companies(limit)

if df.empty:
    st.warning("No company data available.")
else:
    df['short_name'] = df['name'].apply(lambda x: x[:45] + '…' if len(x) > 45 else x)

    fig = px.bar(
        df, x='patent_count', y='short_name', orientation='h',
        color='patent_count', color_continuous_scale='Blues',
        labels={'patent_count': 'Number of Patents', 'short_name': 'Company'},
        height=max(450, limit * 24)
    )
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter, sans-serif', color='#334155'),
        title=dict(text=f'Top {limit} Companies by Patent Count', font=dict(size=15, color='#0d2b5e')),
        yaxis=dict(categoryorder='total ascending', gridcolor='#f1f5f9'),
        xaxis=dict(gridcolor='#f1f5f9', title='Number of Patents'),
        coloraxis_showscale=False,
        margin=dict(t=60, b=40, l=40, r=20),
        hoverlabel=dict(bgcolor='#0d2b5e', font_color='white')
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.markdown("#### 📋 Full Data Table")
    st.dataframe(
        df[['name', 'patent_count']].rename(columns={'name': 'Company', 'patent_count': 'Patents'}),
        width='stretch', hide_index=True
    )
