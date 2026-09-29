"""
db_setup.py  –  Database initialisation and helper queries.

Creates three tables on first run:
    1. users       – stores registered usernames and hashed passwords
    2. questions   – stores the MCQ question bank
    3. scores      – stores quiz scores for the leaderboard

All functions accept / return plain Python types so the rest of the
app never touches raw SQL.
"""

import sqlite3
import os
from database.questions_data import QUESTIONS

# Store the database file alongside this module
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "quiz_app.db")


# ──────────────────── CONNECTION HELPER ────────────────────
def get_connection():
    """Return a new SQLite connection to the quiz database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")   # enable FK support
    return conn


# ──────────────────── TABLE CREATION ────────────────────
def create_tables():
    """Create all required tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL
        )
    """)

    # Questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            question        TEXT    NOT NULL,
            option_a        TEXT    NOT NULL,
            option_b        TEXT    NOT NULL,
            option_c        TEXT    NOT NULL,
            option_d        TEXT    NOT NULL,
            correct_option  TEXT    NOT NULL,
            category        TEXT    NOT NULL,
            difficulty      TEXT    NOT NULL
        )
    """)

    # Scores table (leaderboard)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL,
            score       INTEGER NOT NULL,
            category    TEXT    NOT NULL,
            difficulty  TEXT    NOT NULL,
            total_questions INTEGER NOT NULL,
            correct     INTEGER NOT NULL,
            wrong       INTEGER NOT NULL,
            time_taken  INTEGER NOT NULL,
            date        TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────── SEED QUESTIONS ────────────────────
def seed_questions():
    """
    Insert pre-loaded questions into the database.
    If new questions are added (DB count < list length), it refreshes the questions.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count < len(QUESTIONS):
        cursor.execute("DELETE FROM questions")
        # Reset AUTOINCREMENT if we delete table content
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
        
        cursor.executemany("""
            INSERT INTO questions
                (question, option_a, option_b, option_c, option_d,
                 correct_option, category, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, QUESTIONS)
        conn.commit()
        print(f"[DB] Seeded {len(QUESTIONS)} questions into the database (refreshed).")
    else:
        print(f"[DB] Questions table already has {count} rows – skipping seed.")

    conn.close()


# ──────────────────── USER OPERATIONS ────────────────────
def register_user(username: str, hashed_password: str) -> bool:
    """
    Register a new user. Returns True on success, False if username exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False        # username already taken
    finally:
        conn.close()


def authenticate_user(username: str, hashed_password: str) -> bool:
    """
    Check if a user with the given credentials exists.
    Returns True if valid, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ──────────────────── QUESTION OPERATIONS ────────────────────
def fetch_questions(category: str, difficulty: str, limit: int = 10) -> list:
    """
    Fetch random questions filtered by category and difficulty.
    Returns a list of tuples:
        (id, question, option_a, option_b, option_c, option_d, correct_option)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, correct_option
        FROM questions
        WHERE category = ? AND difficulty = ?
        ORDER BY RANDOM()
        LIMIT ?
    """, (category, difficulty, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ──────────────────── SCORE / LEADERBOARD OPERATIONS ────────────────────
def save_score(username: str, score: int, category: str, difficulty: str,
               total_questions: int, correct: int, wrong: int,
               time_taken: int, date: str):
    """Insert a new score entry after a quiz session."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scores
            (username, score, category, difficulty,
             total_questions, correct, wrong, time_taken, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, score, category, difficulty,
          total_questions, correct, wrong, time_taken, date))
    conn.commit()
    conn.close()


def fetch_leaderboard(limit: int = 10) -> list:
    """
    Fetch the top scores across all categories/difficulties.
    Returns list of tuples:
        (rank, username, score, category, difficulty, date)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, score, category, difficulty, date
        FROM scores
        ORDER BY score DESC, time_taken ASC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    # Add rank numbers
    ranked = [(i + 1, *row) for i, row in enumerate(rows)]
    return ranked


# ──────────────────── INITIALISE ON IMPORT ────────────────────
def initialise_database():
    """One-call setup: creates tables and seeds questions."""
    create_tables()
    seed_questions()
