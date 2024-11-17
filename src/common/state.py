# Filepath: src/state.py
import streamlit as st
import json
import os

def initialize_session_state():
    """Initialize session state variables."""
    # Core game state variables
    if "action_points" not in st.session_state:
        st.session_state.action_points = 3
    if "completed_actions" not in st.session_state:
        st.session_state.completed_actions = []
    if "approval_rating" not in st.session_state:
        st.session_state.approval_rating = 75
    if "stress_level" not in st.session_state:
        st.session_state.stress_level = 25

    # President profile information
    if "president_name" not in st.session_state:
        st.session_state.president_name = "President Alex Harper"
    if "president_image" not in st.session_state:
        st.session_state.president_image = "assets/president.jpg"  # Default image path

    # Cabinet members with default initialization
    if "cabinet_members" not in st.session_state:
        st.session_state.cabinet_members = {
            "Secretary of State": {
                "Name": "Antony Blinken",
                "skills": {"Diplomacy": 9, "Economics": 7, "Security": 5},
                "Profile Picture": None,
                "Backstory": "An experienced diplomat with a history of fostering international alliances.",
                "Motivations": "Seeks to maintain global peace and strengthen economic ties."
            },
            "Secretary of Treasury": {
                "Name": "Janet Yellen",
                "skills": {"Economics": 10, "Public Communication": 7},
                "Profile Picture": None,
                "Backstory": "A renowned economist with decades of expertise in fiscal policy.",
                "Motivations": "Focuses on ensuring financial stability and reducing inequality."
            },
            "Secretary of Defense": {
                "Name": "Lloyd Austin",
                "skills": {"Security": 10, "Strategy": 8, "Logistics": 6},
                "Profile Picture": None,
                "Backstory": "A retired general with extensive experience in military operations.",
                "Motivations": "Dedicated to safeguarding national security and supporting the armed forces."
            },
        }

SAVE_FILE = "cabinet_members.json"

def save_cabinet_members(cabinet_members):
    """Save cabinet members to a JSON file."""
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(cabinet_members, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving cabinet members: {e}")
        return False

def load_cabinet_members():
    """Load cabinet members from a JSON file."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading cabinet members: {e}")
            return {}
    return {}