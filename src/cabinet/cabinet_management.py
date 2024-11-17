import streamlit as st
from src.cabinet.cabinet_db import initialize_database, get_cabinet_members, update_cabinet_member
from src.cabinet.cabinet_utils import get_valid_image_path, save_uploaded_file


def render_cabinet_management():
    """Render the Cabinet Management tab."""
    st.title("Cabinet Management")

    # Initialize the database
    initialize_database()

    # Load cabinet members from the database
    cabinet_members = get_cabinet_members()

    # Editable fields for each cabinet member
    for role, details in cabinet_members.items():
        st.subheader(role)

        # Validate and display profile picture
        profile_picture = get_valid_image_path(details.get("Profile Picture"))
        st.image(profile_picture, caption=details.get("Name", "Unknown"), width=150)

        # File upload for profile picture
        uploaded_file = st.file_uploader(
            f"Upload a picture for {role}", type=["png", "jpg", "jpeg"], key=f"upload_{role}"
        )
        if uploaded_file:
            # Save the uploaded file and update the profile picture path
            saved_path = save_uploaded_file(uploaded_file, role)
            if saved_path:
                details["Profile Picture"] = saved_path  # Update the session state
                st.success(f"Uploaded picture for {role}")
            else:
                st.error(f"Failed to upload picture for {role}")

        # Editable fields
        details["Name"] = st.text_input(
            f"Name for {role}", details.get("Name", "Unknown"), key=f"name_{role}"
        )
        details["Skill"] = st.text_input(
            f"Skill for {role}", details.get("Skill", "Not Specified"), key=f"skill_{role}"
        )
        details["Personality"] = st.text_input(
            f"Personality for {role}", details.get("Personality", "Not Specified"), key=f"personality_{role}"
        )
        details["Expertise"] = st.text_input(
            f"Expertise for {role}", details.get("Expertise", "Not Specified"), key=f"expertise_{role}"
        )
        details["Backstory"] = st.text_area(
            f"Backstory for {role}", details.get("Backstory", "Not Available"), key=f"backstory_{role}"
        )
        details["Motivations"] = st.text_area(
            f"Motivations for {role}", details.get("Motivations", "Not Available"), key=f"motivations_{role}"
        )

        # Add Notes and Links
        details["Notes"] = st.text_area(
            f"Notes about {role}", details.get("Notes", ""), key=f"notes_{role}"
        )
        links = st.text_area(
            f"Relevant Links for {role} (comma-separated URLs)",
            ", ".join(details.get("Links", [])),
            key=f"links_{role}",
        )
        details["Links"] = [link.strip() for link in links.split(",") if link.strip()]

        # Save changes button for this member
        if st.button(f"Save Changes for {role}", key=f"save_{role}"):
            update_cabinet_member(role, details)
            st.success(f"{role} updated successfully!")

        # Consult Cabinet Member
        if st.button(f"Consult with {role}", key=f"consult_{role}"):
            consultation_result = consult_cabinet_member(role, details)
            st.success(consultation_result)


def consult_cabinet_member(role, details):
    """Simulate consulting with a cabinet member."""
    # Generate a response based on the cabinet member's attributes
    response = (
        f"You consulted with {details['Name']}, the {role}. "
        f"With their expertise in {details['Expertise']} and personality described as {details['Personality']}, "
        f"they advise you to focus on {details['Motivations']}."
    )
    return response
