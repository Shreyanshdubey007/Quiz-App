"""
helpers.py  –  Utility / helper functions used across the project.
Includes password hashing, input validation, and common constants.
"""

import hashlib


# ──────────────────── CONSTANTS ────────────────────
CATEGORIES = ["Science", "History", "Sports", "General Knowledge"]
DIFFICULTIES = ["Easy", "Hard"]

POINTS_CORRECT = 10       # points awarded for a correct answer
POINTS_WRONG_EASY = 0     # points deducted on wrong answer (Easy)
POINTS_WRONG_HARD = -5    # points deducted on wrong answer (Hard)

TIME_PER_QUESTION = 15    # seconds allowed per question
QUESTIONS_PER_QUIZ = 10   # number of questions in one quiz session


# ──────────────────── PASSWORD HASHING ────────────────────
def hash_password(password: str) -> str:
    """
    Hash a plain-text password using SHA-256.
    Returns the hexadecimal digest string.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare a plain-text password against its stored hash.
    Returns True if they match.
    """
    return hash_password(plain_password) == hashed_password


# ──────────────────── INPUT VALIDATION ────────────────────
def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username rules:
      • 3–20 characters
      • Only letters, digits, and underscores
    Returns (is_valid, error_message).
    """
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(username) > 20:
        return False, "Username must be at most 20 characters."
    if not username.replace("_", "").isalnum():
        return False, "Username can only contain letters, digits, and underscores."
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password rules:
      • Not empty
    Returns (is_valid, error_message).
    """
    if not password:
        return False, "Password cannot be empty."
    return True, ""


# ──────────────────── FORMATTING HELPERS ────────────────────
def format_time(seconds: int) -> str:
    """Convert total seconds to MM:SS string."""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"
