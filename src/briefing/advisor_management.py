import sqlite3
import os
import streamlit as st
from PIL import Image

UPLOAD_FOLDER = "uploaded_images"
DB_FILE = "database.db"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def fetch_advisors():
    """Fetch all advisors from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM advisors")
    advisors = cursor.fetchall()
    conn.close()
    return advisors


def update_advisor(advisor_id, column, new_value):
    """Update a specific advisor's field in the database."""
    # Validate column name to prevent SQL injection
    valid_columns = {"name", "skill", "personality", "expertise", "backstory", "motivations", "profile_picture"}
    if column not in valid_columns:
        raise ValueError(f"Invalid column name: {column}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE advisors SET {column} = ? WHERE id = ?", (new_value, advisor_id))
    conn.commit()
    conn.close()


def update_advisor_profile_picture(advisor_id, file_path):
    """Update the profile picture path for an advisor in the database."""
    update_advisor(advisor_id, "profile_picture", file_path)


def update_advisor_details(advisor_id, details):
    """Update an advisor's details in the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE advisors
        SET name = ?, skill = ?, personality = ?, expertise = ?, backstory = ?, motivations = ?
        WHERE id = ?
    """, (
        details["name"],
        details["skill"],
        details["personality"],
        details["expertise"],
        details["backstory"],
        details["motivations"],
        advisor_id
    ))
    connection.commit()
    connection.close()


def render_advisor_management():
    """Render the Advisor Management interface."""
    advisors = fetch_advisors()  # Fetch advisors from the database

    st.header("Advisor Management")

    for advisor in advisors:
        advisor_id, name, skill, personality, expertise, backstory, motivations, profile_picture = advisor

        with st.expander(f"{name} - {skill}"):
            # Editable fields
            new_name = st.text_input("Name", value=name, key=f"name_{advisor_id}")
            new_skill = st.text_input("Skill", value=skill, key=f"skill_{advisor_id}")
            new_personality = st.text_area("Personality", value=personality, key=f"personality_{advisor_id}")
            new_expertise = st.text_area("Expertise", value=expertise, key=f"expertise_{advisor_id}")
            new_backstory = st.text_area("Backstory", value=backstory, key=f"backstory_{advisor_id}")
            new_motivations = st.text_area("Motivations", value=motivations, key=f"motivations_{advisor_id}")

            # Display profile picture
            if profile_picture and os.path.exists(profile_picture):
                st.image(profile_picture, caption=new_name, use_column_width=False, width=200)
            else:
                st.image("assets/advisors/default.jpg", caption="Default Image", use_column_width=False, width=200)

            # Allow the user to upload a new profile picture
            uploaded_file = st.file_uploader(f"Upload a new profile picture for {new_name}", type=["png", "jpg", "jpeg"], key=f"upload_{advisor_id}")
            if uploaded_file:
                # Save the uploaded file
                file_path = os.path.join(UPLOAD_FOLDER, f"{advisor_id}_{uploaded_file.name}")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Update the profile picture in the database
                update_advisor_profile_picture(advisor_id, file_path)
                st.success(f"Profile picture for {new_name} updated!")

            # Save changes to other fields
            if st.button(f"Save changes for {new_name}", key=f"save_{advisor_id}"):
                # Update advisor details in the database
                update_advisor_details(advisor_id, {
                    "name": new_name,
                    "skill": new_skill,
                    "personality": new_personality,
                    "expertise": new_expertise,
                    "backstory": new_backstory,
                    "motivations": new_motivations
                })
                st.success(f"Details for {new_name} updated!")
