"""
Shared top navigation bar — import and call render_navbar() on every page.
"""
import streamlit as st
import os

NAVBAR_CSS = """
<style>
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: linear-gradient(90deg, #0d2b5e 0%, #1565c0 100%);
    padding: 0.6rem 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.navbar-brand {
    color: white !important;
    font-weight: 700;
    font-size: 1.1rem;
    margin-right: 1.5rem;
}
/* Push page content down so navbar doesn't overlap */
.block-container {
    padding-top: 4.5rem !important;
}
/* Style navbar buttons */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button {
    background: transparent !important;
    color: rgba(255,255,255,0.85) !important;
    border: none !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.35rem 0.75rem !important;
    border-radius: 6px !important;
    height: auto !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button:hover {
    background: rgba(255,255,255,0.18) !important;
    color: white !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button[kind="primary"] {
    background: rgba(255,255,255,0.22) !important;
    color: white !important;
    font-weight: 600 !important;
}
</style>
"""

def render_navbar(active="overview"):
    st.markdown(NAVBAR_CSS, unsafe_allow_html=True)
    
    st.markdown('<div class="navbar"><span class="navbar-brand">🔬 Patent Intelligence</span></div>', unsafe_allow_html=True)
    
    # Get absolute paths
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create horizontal button row
    cols = st.columns([1, 1.2, 1.2, 1.2, 1, 1])
    
    with cols[0]:
        if st.button("🏠 Overview", use_container_width=True, type="primary" if active == "overview" else "secondary", key="nav_overview"):
            st.switch_page(os.path.join(base, "dashboard.py"))
    with cols[1]:
        if st.button("🏆 Top Inventors", use_container_width=True, type="primary" if active == "inventors" else "secondary", key="nav_inventors"):
            st.switch_page(os.path.join(base, "pages", "1_Top_Inventors.py"))
    with cols[2]:
        if st.button("🏢 Top Companies", use_container_width=True, type="primary" if active == "companies" else "secondary", key="nav_companies"):
            st.switch_page(os.path.join(base, "pages", "2_Top_Companies.py"))
    with cols[3]:
        if st.button("🌍 Top Countries", use_container_width=True, type="primary" if active == "countries" else "secondary", key="nav_countries"):
            st.switch_page(os.path.join(base, "pages", "3_Top_Countries.py"))
    with cols[4]:
        if st.button("📈 Trends", use_container_width=True, type="primary" if active == "trends" else "secondary", key="nav_trends"):
            st.switch_page(os.path.join(base, "pages", "4_Trends.py"))
    with cols[5]:
        if st.button("🔍 Search", use_container_width=True, type="primary" if active == "search" else "secondary", key="nav_search"):
            st.switch_page(os.path.join(base, "pages", "5_Search.py"))
    
    st.markdown("---")


