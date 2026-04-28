import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Top Countries", page_icon="🌍", layout="wide")

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
def get_top_countries(limit):
    return pd.read_sql_query(f"""
        SELECT i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        WHERE i.country != 'Unknown'
        GROUP BY i.country
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
    if st.button("🏢 Top Companies", width='stretch'):
        st.switch_page("pages/2_Top_Companies.py")
    if st.button("🌍 Top Countries", width='stretch', type="primary"):
        st.switch_page("pages/3_Top_Countries.py")
    if st.button("📈 Trends", width='stretch'):
        st.switch_page("pages/4_Trends.py")
    if st.button("🔍 Search Patents", width='stretch'):
        st.switch_page("pages/5_Search.py")

render_navbar(active="countries")

st.markdown("""
<div class="page-header">
    <h2>🌍 Top Countries</h2>
    <p>Countries ranked by total number of granted patents from their inventors</p>
</div>
""", unsafe_allow_html=True)

limit = st.slider("Number of countries to display", 5, 30, 15)
df = get_top_countries(limit)

if df.empty:
    st.warning("No country data available.")
else:
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_bar = px.bar(
            df, x='country', y='patent_count',
            color='patent_count', color_continuous_scale='Blues',
            labels={'patent_count': 'Number of Patents', 'country': 'Country'},
        )
        fig_bar.update_layout(
            paper_bgcolor='white', plot_bgcolor='white',
            font=dict(family='Inter, sans-serif', color='#334155'),
            title=dict(text='Patent Count by Country', font=dict(size=15, color='#0d2b5e')),
            xaxis=dict(gridcolor='#f1f5f9'),
            yaxis=dict(gridcolor='#f1f5f9', title='Number of Patents'),
            coloraxis_showscale=False,
            margin=dict(t=60, b=40, l=40, r=20),
            hoverlabel=dict(bgcolor='#0d2b5e', font_color='white')
        )
        st.plotly_chart(fig_bar, width='stretch')

    with col2:
        fig_pie = px.pie(
            df, values='patent_count', names='country',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor='white',
            font=dict(family='Inter, sans-serif', color='#334155'),
            title=dict(text='Share by Country', font=dict(size=15, color='#0d2b5e')),
            margin=dict(t=60, b=20, l=20, r=20),
            legend=dict(font=dict(size=11))
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, width='stretch')

    st.markdown("---")
    st.markdown("#### 📋 Full Data Table")
    st.dataframe(
        df.rename(columns={'country': 'Country', 'patent_count': 'Patents'}),
        width='stretch', hide_index=True
    )
