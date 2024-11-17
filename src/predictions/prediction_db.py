import sqlite3

DB_PATH = "predictions.db"


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        outcome BOOLEAN DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP
    )
    """)

    # Create User Guesses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_guesses (
        id INTEGER PRIMARY KEY,
        user_id TEXT NOT NULL,
        prediction_id INTEGER NOT NULL,
        user_choice BOOLEAN NOT NULL,
        points_earned INTEGER DEFAULT 0,
        FOREIGN KEY (prediction_id) REFERENCES predictions (id)
    )
    """)

    conn.commit()
    conn.close()


def add_prediction(text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predictions (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()


def update_prediction_outcome(prediction_id, outcome):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE predictions SET outcome = ?, resolved_at = CURRENT_TIMESTAMP WHERE id = ?",
        (outcome, prediction_id),
    )
    conn.commit()
    conn.close()


def get_active_predictions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE outcome IS NULL")
    predictions = cursor.fetchall()
    conn.close()
    return predictions


def submit_user_guess(user_id, prediction_id, user_choice):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_guesses (user_id, prediction_id, user_choice) VALUES (?, ?, ?)",
        (user_id, prediction_id, user_choice),
    )
    conn.commit()
    conn.close()
