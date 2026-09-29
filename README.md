# 🧠 Quiz App with Leaderboard

A Python desktop application built with **Tkinter** (GUI) and **SQLite** (database) for a second-semester project.

---

## 📂 Project Structure

```
Quiz-App/
├── main.py                        # Entry point – run this to start the app
├── README.md                      # Project documentation
│
├── database/                      # Database layer
│   ├── __init__.py
│   ├── db_setup.py                # SQLite table creation, CRUD functions
│   └── questions_data.py          # Pre-loaded 40 MCQ questions
│
├── screens/                       # GUI screens (Tkinter Frames)
│   ├── __init__.py
│   ├── login_screen.py            # Login / Register screen
│   ├── home_screen.py             # Main menu (Start Quiz, Leaderboard, Logout)
│   ├── quiz_setup_screen.py       # Category & Difficulty selection
│   ├── quiz_screen.py             # Quiz session (timer, options, scoring)
│   ├── result_screen.py           # Results summary after quiz
│   └── leaderboard_screen.py      # Top 10 scores table
│
└── utils/                         # Utilities & helpers
    ├── __init__.py
    └── helpers.py                 # Password hashing, validation, constants
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **User Authentication** | Register & Login with SHA-256 hashed passwords |
| **Category Selection** | Science, History, Sports, General Knowledge |
| **Difficulty Levels** | Easy (+10 correct, 0 wrong) and Hard (+10 correct, −5 wrong) |
| **Countdown Timer** | 15-second timer per question using `after()` |
| **Answer Feedback** | Correct → green, Wrong → red, shows correct answer |
| **Results Screen** | Score, accuracy %, correct/wrong count, time taken |
| **Leaderboard** | Top 10 scores with Treeview – gold/silver/bronze highlighting |
| **40 Pre-loaded MCQs** | 5 Easy + 5 Hard for each of the 4 categories |

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** – GUI framework (built-in with Python)
- **SQLite3** – Lightweight database (built-in with Python)
- **hashlib** – Password hashing (built-in with Python)

> No external packages are required. Everything uses Python's standard library.

---

## 🚀 How to Run

1. Make sure Python 3.x is installed on your system.
2. Open a terminal/command prompt in the project directory.
3. Run:

```bash
python main.py
```

The application window will open with the Login screen.

---

## 🗄️ Database Schema

### `users` table
| Column | Type | Description |
|---|---|---|
| id | INTEGER (PK) | Auto-increment ID |
| username | TEXT (UNIQUE) | User's display name |
| password | TEXT | SHA-256 hashed password |

### `questions` table
| Column | Type | Description |
|---|---|---|
| id | INTEGER (PK) | Auto-increment ID |
| question | TEXT | The question text |
| option_a | TEXT | Option A |
| option_b | TEXT | Option B |
| option_c | TEXT | Option C |
| option_d | TEXT | Option D |
| correct_option | TEXT | Correct answer (A/B/C/D) |
| category | TEXT | Science / History / Sports / General Knowledge |
| difficulty | TEXT | Easy / Hard |

### `scores` table (Leaderboard)
| Column | Type | Description |
|---|---|---|
| id | INTEGER (PK) | Auto-increment ID |
| username | TEXT | Player's username |
| score | INTEGER | Final score |
| category | TEXT | Quiz category played |
| difficulty | TEXT | Difficulty level |
| total_questions | INTEGER | Total questions in the session |
| correct | INTEGER | Number answered correctly |
| wrong | INTEGER | Number answered wrong |
| time_taken | INTEGER | Total seconds taken |
| date | TEXT | Date and time of the quiz |

---

## 📸 Screens Flow

```
Login/Register  →  Home Menu  →  Quiz Setup  →  Quiz Session  →  Results
                       ↓                                            ↓
                  Leaderboard                                  Save Score
```

---

## 👨‍💻 Author

Shreyansh – Second Semester Project (2026)
