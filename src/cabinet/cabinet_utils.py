import random
import os
import json
from src.cabinet.cabinet_defaults import CABINET_OPTIONS

# Constants
DEFAULT_SKILLS = ["Diplomacy", "Economics", "Security", "Legal Expertise", "Public Communication"]
SAVE_FILE = "cabinet_members.json"
IMAGE_DIR = "uploaded_images"
os.makedirs(IMAGE_DIR, exist_ok=True)  # Ensure the directory exists

# Ensure necessary directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)


def assign_skills_randomly():
    """Assign random DnD-style skill levels (3-18) to cabinet members."""
    return {skill: random.randint(3, 18) for skill in DEFAULT_SKILLS}


def initialize_cabinet_member(role, name):
    """Initialize a cabinet member with defaults from CABINET_OPTIONS."""
    # Retrieve the defaults for the role
    defaults = CABINET_OPTIONS.get(role, {})
    if not defaults:
        raise ValueError(f"No defaults found for the role: {role}")

    # Ensure all necessary keys exist
    member_details = {
        "Name": name,
        "Skill": defaults.get("Skill", "Not Specified"),
        "Personality": defaults.get("Personality", "Not Specified"),
        "Expertise": defaults.get("Expertise", "Not Specified"),
        "Backstory": defaults.get("Backstory", f"Default backstory for {name}."),
        "Motivations": defaults.get("Motivations", f"Default motivations for {name}."),
        "Profile Picture": defaults.get("Profile Picture", None),
        "Skills": assign_skills_randomly(),  # Add random skill stats
    }
    return member_details


def ensure_member_details(member_details, role, selected_member):
    """Ensure runtime-specific fields exist for a cabinet member."""
    member_details.setdefault("Profile Picture", None)
    member_details.setdefault("Skills", assign_skills_randomly())
    return member_details





def save_uploaded_file(uploaded_file, member_name):
    """Save uploaded profile picture to a file."""
    file_extension = os.path.splitext(uploaded_file.name)[1]
    if file_extension.lower() not in [".png", ".jpg", ".jpeg"]:
        return None
    file_path = os.path.join(IMAGE_DIR, f"{member_name.replace(' ', '_')}{file_extension}")
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        print(f"Error saving file for {member_name}: {e}")
        return None


def save_cabinet_members(cabinet_members):
    """Save cabinet members to a JSON file."""
    sanitized_members = {
        role: {
            key: details[key]
            for key in ["Name", "Skill", "Personality", "Expertise", "Backstory", "Motivations", "Profile Picture", "Skills"]
            if key in details
        }
        for role, details in cabinet_members.items()
    }
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(sanitized_members, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving cabinet members: {e}")
        return False



def load_cabinet_members():
    """Load cabinet members from a JSON file and ensure defaults."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                members = json.load(file)
                # Ensure all fields exist
                for role, details in members.items():
                    defaults = CABINET_OPTIONS.get(role, {})
                    for key, value in defaults.items():
                        details.setdefault(key, value)
                    # Ensure skills are always present
                    if "Skills" not in details:
                        details["Skills"] = assign_skills_randomly()
                return members
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading cabinet members: {e}")
            return {}
    return {}


def get_valid_image_path(image_path):
    """Return a valid image path or fallback to the default."""
    if image_path and os.path.exists(image_path):
        return image_path
    # Fallback to default shadow profile
    return "assets/shadow_profile.jpeg"
