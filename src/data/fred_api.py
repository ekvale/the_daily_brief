print("Filepath: src/fred_api.py")


import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_data(series_id, start_date="2020-01-01"):
    """Fetch data from the FRED API for a given series."""
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "observations" in data:
            latest = data["observations"][-1]  # Get the latest observation
            return float(latest["value"]), latest["date"]
        else:
            st.error(f"No data found for series {series_id}.")
            return None, None
    except requests.RequestException as e:
        st.error(f"Error fetching data from FRED: {e}")
        return None, None

def fetch_gdp_growth():
    """Fetch recent GDP growth data."""
    series_id = "GDP"  # Replace with the specific FRED series ID for GDP growth
    value, date = fetch_fred_data(series_id)
    if value:
        return f"{value:.2f}%", date
    return "N/A", None

def fetch_unemployment_rate():
    """Fetch recent unemployment rate data."""
    series_id = "UNRATE"  # Replace with the FRED series ID for unemployment rate
    value, date = fetch_fred_data(series_id)
    if value:
        return f"{value:.1f}%", date
    return "N/A", None