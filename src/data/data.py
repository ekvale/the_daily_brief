# Filepath: src/data.py

import requests
import pandas as pd
import streamlit as st
from src.data.fred_api import API_KEY, BASE_URL
import wbgapi as wb
import matplotlib.pyplot as plt

# ------------------- FRED API FUNCTIONS -------------------

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
            # Convert observations into a DataFrame
            observations = pd.DataFrame(data["observations"])
            observations["value"] = pd.to_numeric(observations["value"], errors="coerce")
            observations["date"] = pd.to_datetime(observations["date"])
            return observations[["date", "value"]]
        else:
            st.error(f"No data found for series {series_id}.")
            return pd.DataFrame(columns=["date", "value"])
    except requests.RequestException as e:
        st.error(f"Error fetching data from FRED: {e}")
        return pd.DataFrame(columns=["date", "value"])

def get_economic_data():
    """Fetch and process multiple economic indicators from the FRED API."""
    indicators = {
        "GDP Growth Rate (%)": "A191RL1Q225SBEA",  # Real GDP growth rate (quarterly)
        "Inflation Rate (%)": "CPIAUCSL",  # Consumer Price Index (monthly)
        "Unemployment Rate (%)": "UNRATE",  # Unemployment rate (monthly)
    }

    data_frames = {}

    for name, series_id in indicators.items():
        df = fetch_fred_data(series_id)
        if name == "Inflation Rate (%)":
            # Calculate percentage change for CPI to derive annualized inflation rate
            df["value"] = df["value"].pct_change(periods=12) * 100  # Annual % change
        data_frames[name] = df.rename(columns={"value": name})

    # Align all data to the same frequency and merge
    merged_data = data_frames["GDP Growth Rate (%)"]  # Start with GDP (quarterly)
    for name, df in data_frames.items():
        if name != "GDP Growth Rate (%)":  # Merge other indicators
            merged_data = pd.merge(merged_data, df, on="date", how="outer")

    # Sort data by date, fill missing values for alignment
    merged_data.sort_values("date", inplace=True)
    merged_data.set_index("date", inplace=True)
    merged_data.interpolate(method="time", inplace=True)  # Fill missing values
    return merged_data

# ------------------- WORLD BANK API FUNCTIONS -------------------

def fetch_global_gdp_data(countries, start_year=2000, end_year=2024):
    """Fetch GDP per capita for a list of countries over a specified range of years."""
    try:
        # Fetch GDP per capita (indicator: NY.GDP.PCAP.CD)
        data = wb.data.DataFrame(
            'NY.GDP.PCAP.CD',  # GDP per capita indicator
            countries,         # List of country codes
            time=range(start_year, end_year + 1),  # Time range
            index='time'       # Use time as the DataFrame index
        )
        return data
    except Exception as e:
        print(f"Error fetching GDP per capita data: {e}")
        return pd.DataFrame()

