import streamlit as st
from src.common.state import initialize_session_state
from src.common.sidebar import render_sidebar
from src.briefing.briefing import render_morning_briefing
from src.cabinet.cabinet_selection import render_cabinet_selection
from src.cabinet.cabinet_management import render_cabinet_management
from src.data.data_tab import render_data_tab
from src.config.rss_feeds import RSS_FEEDS
from src.cabinet.cabinet_utils import load_cabinet_members
from src.cabinet.cabinet_db import initialize_database, get_cabinet_members
from src.predictions.prediction_admin import admin_tab
from src.predictions.prediction_user import user_tab
from src.briefing.advisor_management import render_advisor_management
from dotenv import load_dotenv

# Initialize database and load data into session state
initialize_database()

# Initialize session state variables for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

# Static credentials for login
STATIC_USERNAME = "admin"
STATIC_PASSWORD = "password"

# Define the login page
def login_page():
    st.title("Welcome to The Daily Briefing")
    st.markdown("**Log in to start managing your presidential duties.**")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == STATIC_USERNAME and password == STATIC_PASSWORD:
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")

# Define the main app interface
def main_app():
    # Load cabinet members into session state
    if "cabinet_members" not in st.session_state:
        st.session_state.cabinet_members = get_cabinet_members()

    initialize_session_state()

    if "cabinet_members" not in st.session_state or not st.session_state.cabinet_members:
        st.session_state.cabinet_members = load_cabinet_members()

    # Sidebar
    render_sidebar()

    # Tabs for navigation
    TABS = [
        "Morning Briefing",
        "Cabinet Selection",
        "Cabinet Management",
        "Advisor Management",
        "National and Global Data",  # Fixed comma
        "Prediction Game",
        "Admin Panel"
    ]
    tabs = st.tabs(TABS)

    # Tab 0: Morning Briefing
    with tabs[0]:
        render_morning_briefing(RSS_FEEDS, st.session_state.cabinet_members)

    # Tab 1: Cabinet Selection
    with tabs[1]:
        render_cabinet_selection()

    # Tab 2: Cabinet Management
    with tabs[2]:
        render_cabinet_management()

    # Tab 3: Advisor Management
    with tabs[3]:
        render_advisor_management()

    # Tab 4: National and Global Data
    with tabs[4]:
        render_data_tab()

    # Tab 5: Prediction Game
    with tabs[5]:
        user_tab()

    # Tab 6: Admin Panel
    with tabs[6]:
        admin_tab()


# Main logic
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
