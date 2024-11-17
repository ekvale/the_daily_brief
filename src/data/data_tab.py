# Filepath: src/data_tab.py

import streamlit as st
import matplotlib.pyplot as plt
from src.data.data import get_economic_data, fetch_global_gdp_data, fetch_fred_data


def render_data_tab():
    """Render the National and Global Data tab."""
    st.title("National and Global Data")

    # ECONOMIC INDICATORS FROM FRED
    st.header("Economic Indicators (FRED)")
    economic_data = get_economic_data()

    if not economic_data.empty:
        for column in economic_data.columns:
            st.subheader(f"{column} Over Time")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(economic_data.index, economic_data[column], label=column, color="blue")
            ax.set_title(f"{column} Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel(column)
            ax.legend()
            st.pyplot(fig)
    else:
        st.error("Failed to load economic data. Please check the FRED API integration.")

    # REAL WAGES
    st.header("Real Wages (FRED)")
    nominal_wages = fetch_fred_data("CES0500000003")  # Average hourly earnings
    cpi = fetch_fred_data("CPIAUCSL")  # Consumer Price Index

    if not nominal_wages.empty and not cpi.empty:
        # Merge data and calculate real wages
        real_wages = nominal_wages.merge(cpi, on="date", suffixes=("_nominal", "_cpi"))
        real_wages["Real Wages"] = (real_wages["value_nominal"] / real_wages["value_cpi"]) * 100

        # Plot real wages
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(real_wages["date"], real_wages["Real Wages"], label="Real Wages", color="green")
        ax.set_title("Real Wages Over Time", fontsize=16)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Real Wages (Indexed)", fontsize=12)
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Failed to load data for Real Wages. Please check the FRED API integration.")

    # GLOBAL ECONOMIC INDICATORS FROM WORLD BANK
    st.header("Global Economic Indicators")
    st.subheader("GDP Per Capita (Current US$)")

    # List of countries: USA and the 10 largest economies by GDP
    countries = ['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR', 'FRA', 'ITA', 'BRA', 'CAN', 'KOR']
    country_names = {
        'USA': 'United States',
        'CHN': 'China',
        'JPN': 'Japan',
        'DEU': 'Germany',
        'IND': 'India',
        'GBR': 'United Kingdom',
        'FRA': 'France',
        'ITA': 'Italy',
        'BRA': 'Brazil',
        'CAN': 'Canada',
        'KOR': 'South Korea'
    }

    gdp_data = fetch_global_gdp_data(countries)

    if not gdp_data.empty:
        # Plot the GDP per capita data
        fig, ax = plt.subplots(figsize=(12, 7))
        gdp_data.rename(columns=country_names).plot(ax=ax)
        ax.set_title("GDP Per Capita (2000-2024)", fontsize=16)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("GDP Per Capita (Current US$)", fontsize=12)
        ax.legend(country_names.values(), title="Countries")
        st.pyplot(fig)
    else:
        st.error("Failed to load GDP per capita data. Please check the World Bank API integration.")




