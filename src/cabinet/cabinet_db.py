import sqlite3
from src.cabinet.cabinet_defaults import CABINET_OPTIONS

DB_FILE = "cabinet_members.db"

def initialize_database():
    """Initialize the database with the required table and ensure all columns exist."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

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
            skills TEXT
        )
    """)

    # Add missing columns for notes and links
    try:
        cursor.execute("ALTER TABLE cabinet_members ADD COLUMN notes TEXT")
    except sqlite3.OperationalError:
        # Column already exists
        pass

    try:
        cursor.execute("ALTER TABLE cabinet_members ADD COLUMN links TEXT")
    except sqlite3.OperationalError:
        # Column already exists
        pass

    connection.commit()
    connection.close()


    # Populate database with default values if empty
    populate_defaults()


def populate_defaults():
    """Populate the database with default values if no records exist."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Check if the table is already populated
    cursor.execute("SELECT COUNT(*) FROM cabinet_members")
    if cursor.fetchone()[0] == 0:
        for role, details in CABINET_OPTIONS.items():
            skills = "{}"  # Placeholder for skills JSON (to be implemented)
            cursor.execute("""
                INSERT INTO cabinet_members (role, name, skill, personality, expertise, backstory, motivations, profile_picture, skills)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                role,
                details.get("Name", "Unknown"),
                details.get("Skill", "Not Specified"),
                details.get("Personality", "Not Specified"),
                details.get("Expertise", "Not Specified"),
                details.get("Backstory", "Not Available"),
                details.get("Motivations", "Not Available"),
                details.get("Profile Picture", None),
                skills
            ))
    connection.commit()
    connection.close()


def get_cabinet_members():
    """Retrieve all cabinet members from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cabinet_members")
    rows = cursor.fetchall()

    connection.close()

    # Convert rows to a dictionary for easier handling
    members = {
        row[0]: {
            "Name": row[1],
            "Skill": row[2],
            "Personality": row[3],
            "Expertise": row[4],
            "Backstory": row[5],
            "Motivations": row[6],
            "Profile Picture": row[7],
            "Skills": eval(row[8]) if row[8] else {},  # Convert stringified JSON to dictionary
            "Notes": row[9] if len(row) > 9 else "",  # Handle missing Notes
            "Links": row[10].split(", ") if len(row) > 10 and row[10] else []  # Convert string to list
        }
        for row in rows
    }
    return members



def update_cabinet_member(role, details):
    """Update a cabinet member's details in the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    skills = str(details.get("Skills", {}))  # Convert dictionary to string for storage
    links = ", ".join(details.get("Links", []))  # Convert list of links to comma-separated string
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

