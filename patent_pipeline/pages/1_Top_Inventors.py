import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Top Inventors", page_icon="🏆", layout="wide")

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
def get_top_inventors(limit):
    return pd.read_sql_query(f"""
        SELECT i.name, i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        GROUP BY i.inventor_id, i.name, i.country
        ORDER BY patent_count DESC
        LIMIT {limit}
    """, get_conn())

# ── Sidebar nav ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Patent Intel")
    st.markdown("---")
    if st.button("🏠 Overview", use_container_width=True):
        st.switch_page("dashboard.py")
    if st.button("🏆 Top Inventors", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Top_Inventors.py")
    if st.button("🏢 Top Companies", use_container_width=True):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", use_container_width=True):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", use_container_width=True):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", use_container_width=True):
        st.switch_page("pages/5_Search.py")

render_navbar(active="inventors")

# ── Page content ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h2>🏆 Top Inventors</h2>
    <p>Inventors ranked by total number of granted patents</p>
</div>
""", unsafe_allow_html=True)

limit = st.slider("Number of inventors to display", 5, 50, 20)
df = get_top_inventors(limit)

if df.empty:
    st.warning("No inventor data available.")
else:
    # Colorful palette — one distinct color per country
    fig = px.bar(
        df, x='patent_count', y='name', orientation='h',
        color='country',
        labels={'patent_count': 'Number of Patents', 'name': 'Inventor', 'country': 'Country'},
        height=max(450, limit * 24),
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter, sans-serif', color='#334155'),
        title=dict(text=f'Top {limit} Inventors by Patent Count', font=dict(size=15, color='#0d2b5e')),
        yaxis=dict(categoryorder='total ascending', gridcolor='#f1f5f9'),
        xaxis=dict(gridcolor='#f1f5f9', title='Number of Patents'),
        legend=dict(title='Country', orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=60, b=40, l=40, r=20),
        hoverlabel=dict(bgcolor='#0d2b5e', font_color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Full Data Table")
    st.dataframe(
        df.rename(columns={'name': 'Inventor', 'country': 'Country', 'patent_count': 'Patents'}),
        use_container_width=True, hide_index=True
    )
