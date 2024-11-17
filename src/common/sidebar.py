# Filepath: src/sidebar.py

import streamlit as st
from src.common.advisors import advisors
from src.data.fred_api import fetch_fred_data

def render_sidebar():
    """Render the sidebar with president profile, national statistics, and advisors."""
    st.sidebar.image(st.session_state.president_image, width=150)  # Profile picture
    st.sidebar.title("President Profile")
    st.sidebar.write(f"Name: {st.session_state.president_name}")
    st.sidebar.write(f"Approval Rating: {st.session_state.approval_rating}%")
    st.sidebar.write(f"Stress Level: {st.session_state.stress_level}%")
    st.sidebar.write(f"Action Points: {st.session_state.action_points}")

    # National Statistics Section
    st.sidebar.write("### National Statistics")
    indicators = {
        "GDP Growth Rate": "GDP",
        "Unemployment Rate": "UNRATE",
        "Inflation Rate": "CPIAUCSL",
        "Federal Debt": "GFDEBTN",
    }
    for stat, series_id in indicators.items():
        value, date = fetch_fred_data(series_id)
        if value is not None:
            st.sidebar.write(f"{stat}: {value:.2f} (as of {date})")

    # Advisors Section
    st.sidebar.write("### Presidential Advisors")
    for role, info in advisors.items():
        st.sidebar.write(f"**{role}**: {info['Name']} ({info['Skill']})")