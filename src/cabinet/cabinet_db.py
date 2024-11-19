import sqlite3
import json
import os
from src.common.advisors import advisors  # Import data from advisors.py

DB_FILE = "database.db"
UPLOAD_FOLDER = "uploaded_images"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def initialize_database():
    """Initialize the database with the required tables and populate initial data."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create the advisors table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advisors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            skill TEXT,
            personality TEXT,
            expertise TEXT,
            backstory TEXT,
            motivations TEXT
        )
    """)

    # Add the profile_picture column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE advisors ADD COLUMN profile_picture TEXT")
    except sqlite3.OperationalError:
        # Column already exists
        pass

    # Create the cabinet_members table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cabinet_members (
            role TEXT PRIMARY KEY,
            name TEXT,
            skill TEXT,
            personality TEXT,
            expertise TEXT,
            backstory TEXT,
            motivations TEXT,
            profile_picture TEXT,
            skills TEXT,
            notes TEXT,
            links TEXT
        )
    """)

    connection.commit()

    # Populate initial advisors if the table is empty
    cursor.execute("SELECT COUNT(*) FROM advisors")
    if cursor.fetchone()[0] == 0:
        populate_advisors_from_file(cursor)

    connection.commit()
    connection.close()



def populate_advisors_from_file(cursor):
    """Populate the advisors table with data from advisors.py."""
    for advisor_role, details in advisors.items():
        cursor.execute("""
            INSERT INTO advisors (name, skill, personality, expertise, backstory, motivations, profile_picture)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            details.get("Name", "Unknown"),
            details.get("Skill", "Not Specified"),
            details.get("Personality", "Not Specified"),
            details.get("Expertise", "Not Specified"),
            details.get("Backstory", "Not Available"),
            details.get("Motivations", "Not Available"),
            details.get("ProfilePicture", None)  # Use None if no image is defined
        ))


def get_advisors():
    """Retrieve all advisors from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, skill, personality, expertise, backstory, motivations, profile_picture FROM advisors")
    advisors = cursor.fetchall()
    connection.close()
    return advisors


def update_advisor_profile_picture(advisor_id, uploaded_file):
    """Update the profile picture of an advisor."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Save the uploaded file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, f"{advisor_id}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Update the database with the file path
    cursor.execute("""
        UPDATE advisors
        SET profile_picture = ?
        WHERE id = ?
    """, (file_path, advisor_id))
    connection.commit()
    connection.close()


def get_cabinet_members():
    """Retrieve all cabinet members from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cabinet_members")
    rows = cursor.fetchall()
    connection.close()

    return {
        row[0]: {
            "Name": row[1],
            "Skill": row[2],
            "Personality": row[3],
            "Expertise": row[4],
            "Backstory": row[5],
            "Motivations": row[6],
            "Profile Picture": row[7],
            "Skills": json.loads(row[8]) if row[8] else {},
            "Notes": row[9] if len(row) > 9 else "",
            "Links": row[10].split(", ") if len(row) > 10 and row[10] else []
        }
        for row in rows
    }


def update_cabinet_member(role, details):
    """Update a cabinet member's details in the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    skills = json.dumps(details.get("Skills", {}))
    links = ", ".join(details.get("Links", []))
    cursor.execute("""
        UPDATE cabinet_members
        SET name = ?, skill = ?, personality = ?, expertise = ?, backstory = ?, 
            motivations = ?, profile_picture = ?, skills = ?, notes = ?, links = ?
        WHERE role = ?
    """, (
        details["Name"],
        details["Skill"],
        details["Personality"],
        details["Expertise"],
        details["Backstory"],
        details["Motivations"],
        details["Profile Picture"],
        skills,
        details.get("Notes", ""),
        links,
        role
    ))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
