import streamlit as st
from src.cabinet.cabinet_selection import render_cabinet_selection
from src.cabinet.cabinet_management import render_cabinet_management


def render_cabinet_page(tab="selection"):
    """Render the appropriate cabinet page based on the selected tab."""
    if tab == "selection":
        render_cabinet_selection()
    elif tab == "management":
        render_cabinet_management()
    else:
        st.error("Invalid cabinet tab selected.")
