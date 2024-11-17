import streamlit as st
from src.cabinet.cabinet_utils import initialize_cabinet_member, get_valid_image_path
from src.cabinet.cabinet_defaults import CABINET_OPTIONS


def render_cabinet_selection():
    """Render the Cabinet Selection tab."""
    st.title("Cabinet Selection")

    # Ensure cabinet_members is in session state
    if "cabinet_members" not in st.session_state:
        st.session_state.cabinet_members = {}

    # Add the "Choose Your Cabinet Members" area inside an expander
    with st.expander("Choose Your Cabinet Members", expanded=False):
        st.write("### Select Your Cabinet Members")
        for role, defaults in CABINET_OPTIONS.items():
            # Pre-select the member if already chosen
            current_name = st.session_state.cabinet_members.get(role, {}).get("Name", defaults["Name"])
            selected_member = st.selectbox(f"{role}:", [current_name], key=f"{role}_dropdown")

            # Initialize or update cabinet member details
            if role not in st.session_state.cabinet_members:
                st.session_state.cabinet_members[role] = initialize_cabinet_member(role, selected_member)
            else:
                st.session_state.cabinet_members[role]["Name"] = selected_member

    # Display profiles for all selected cabinet members
    st.write("### Current Cabinet Members")
    for role, details in st.session_state.cabinet_members.items():
        display_cabinet_member(role, details)


def display_cabinet_member(role, details):
    """Display the profile of a selected cabinet member."""
    st.subheader(role)

    # Get valid profile picture path
    profile_picture = get_valid_image_path(details.get("Profile Picture"))

    # Display the profile picture
    st.image(profile_picture, caption=details.get("Name", "Unknown"), width=150)

    # Display all key characteristics with defaults if missing
    st.write(f"**Name:** {details.get('Name', 'Unknown')}")
    st.write(f"**Skill:** {details.get('Skill', 'Not Specified')}")
    st.write(f"**Personality:** {details.get('Personality', 'Not Specified')}")
    st.write(f"**Expertise:** {details.get('Expertise', 'Not Specified')}")
    st.write(f"**Backstory:** {details.get('Backstory', 'Not Available')}")
    st.write(f"**Motivations:** {details.get('Motivations', 'Not Available')}")
