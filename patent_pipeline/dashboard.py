"""
Patent Intelligence Dashboard
Interactive web app built with Streamlit for exploring patent data.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Patent Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = os.path.join(os.path.dirname(__file__), 'patent_pipeline.db')

# ── Database Connection ────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    if not os.path.exists(DB_PATH):
        st.error(f"Database not found at {DB_PATH}. Run the pipeline first.")
        st.stop()
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def run_query(sql):
    conn = get_connection()
    return pd.read_sql_query(sql, conn)

# ── Queries ────────────────────────────────────────────────────────────────────
def get_summary_stats():
    return run_query("""
        SELECT 
            (SELECT COUNT(*) FROM patents) AS total_patents,
            (SELECT COUNT(*) FROM inventors) AS total_inventors,
            (SELECT COUNT(*) FROM companies) AS total_companies,
            (SELECT COUNT(DISTINCT country) FROM inventors WHERE country != 'Unknown') AS total_countries
    """).iloc[0]

def get_top_inventors(limit=20):
    return run_query(f"""
        SELECT i.name, i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        GROUP BY i.inventor_id, i.name, i.country
        ORDER BY patent_count DESC
        LIMIT {limit}
    """)

def get_top_companies(limit=20):
    return run_query(f"""
        SELECT c.name, COUNT(pc.patent_id) AS patent_count
        FROM companies c
        JOIN patent_company pc ON c.company_id = pc.company_id
        GROUP BY c.company_id, c.name
        ORDER BY patent_count DESC
        LIMIT {limit}
    """)

def get_top_countries(limit=15):
    return run_query(f"""
        SELECT i.country, COUNT(pi.patent_id) AS patent_count
        FROM inventors i
        JOIN patent_inventor pi ON i.inventor_id = pi.inventor_id
        WHERE i.country != 'Unknown'
        GROUP BY i.country
        ORDER BY patent_count DESC
        LIMIT {limit}
    """)

def get_trends():
    return run_query("""
        SELECT year, COUNT(*) AS patent_count
        FROM patents
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year
    """)

def search_patents(query):
    return run_query(f"""
        SELECT patent_id, title, year
        FROM patents
        WHERE title LIKE '%{query}%'
        LIMIT 100
    """)

# ── UI Components ──────────────────────────────────────────────────────────────
def render_header():
    st.title("📊 Global Patent Intelligence Dashboard")
    st.markdown("Explore patent data from the USPTO PatentsView database")
    st.divider()

def render_summary():
    stats = get_summary_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patents", f"{int(stats['total_patents']):,}")
    with col2:
        st.metric("Total Inventors", f"{int(stats['total_inventors']):,}")
    with col3:
        st.metric("Total Companies", f"{int(stats['total_companies']):,}")
    with col4:
        st.metric("Countries", f"{int(stats['total_countries']):,}")
    
    st.divider()

def render_top_inventors():
    st.subheader("🏆 Top Inventors")
    
    limit = st.slider("Number of inventors to show", 5, 50, 20, key="inv_slider")
    df = get_top_inventors(limit)
    
    if df.empty:
        st.warning("No inventor data available")
        return
    
    fig = px.bar(
        df, 
        x='patent_count', 
        y='name',
        orientation='h',
        color='country',
        title=f'Top {limit} Inventors by Patent Count',
        labels={'patent_count': 'Number of Patents', 'name': 'Inventor'},
        height=max(400, limit * 20)
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 View Data Table"):
        st.dataframe(df, use_container_width=True)

def render_top_companies():
    st.subheader("🏢 Top Companies")
    
    limit = st.slider("Number of companies to show", 5, 50, 20, key="comp_slider")
    df = get_top_companies(limit)
    
    if df.empty:
        st.warning("No company data available")
        return
    
    fig = px.bar(
        df,
        x='patent_count',
        y='name',
        orientation='h',
        title=f'Top {limit} Companies by Patent Count',
        labels={'patent_count': 'Number of Patents', 'name': 'Company'},
        color='patent_count',
        color_continuous_scale='Blues',
        height=max(400, limit * 20)
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 View Data Table"):
        st.dataframe(df, use_container_width=True)

def render_top_countries():
    st.subheader("🌍 Top Countries")
    
    limit = st.slider("Number of countries to show", 5, 30, 15, key="country_slider")
    df = get_top_countries(limit)
    
    if df.empty:
        st.warning("No country data available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bar = px.bar(
            df,
            x='country',
            y='patent_count',
            title='Patent Count by Country',
            labels={'patent_count': 'Number of Patents', 'country': 'Country'},
            color='patent_count',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_pie = px.pie(
            df,
            values='patent_count',
            names='country',
            title='Patent Distribution by Country'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with st.expander("📋 View Data Table"):
        st.dataframe(df, use_container_width=True)

def render_trends():
    st.subheader("📈 Patent Trends Over Time")
    
    df = get_trends()
    
    if df.empty:
        st.warning("No trend data available")
        return
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['patent_count'],
        mode='lines+markers',
        name='Patents',
        line=dict(color='#2196F3', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.1)'
    ))
    
    fig.update_layout(
        title='Patent Filings Over Time',
        xaxis_title='Year',
        yaxis_title='Number of Patents',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 View Data Table"):
        st.dataframe(df, use_container_width=True)

def render_search():
    st.subheader("🔍 Search Patents")
    
    query = st.text_input("Search by patent title", placeholder="e.g., machine learning, battery, semiconductor")
    
    if query:
        df = search_patents(query)
        
        if df.empty:
            st.info(f"No patents found matching '{query}'")
        else:
            st.success(f"Found {len(df)} patents matching '{query}'")
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "patent_id": "Patent ID",
                    "title": st.column_config.TextColumn("Title", width="large"),
                    "year": "Year"
                }
            )

# ── Main App ───────────────────────────────────────────────────────────────────
def main():
    render_header()
    render_summary()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a view:",
        ["Overview", "Top Inventors", "Top Companies", "Top Countries", "Trends", "Search Patents"]
    )
    
    st.sidebar.divider()
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard visualizes patent data from the USPTO PatentsView database. "
        "Use the navigation to explore different aspects of the data."
    )
    
    # Render selected page
    if page == "Overview":
        col1, col2 = st.columns(2)
        with col1:
            render_top_inventors()
        with col2:
            render_top_companies()
        render_trends()
    elif page == "Top Inventors":
        render_top_inventors()
    elif page == "Top Companies":
        render_top_companies()
    elif page == "Top Countries":
        render_top_countries()
    elif page == "Trends":
        render_trends()
    elif page == "Search Patents":
        render_search()

if __name__ == '__main__':
    main()
