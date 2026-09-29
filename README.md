# 🧠 Quiz App with Leaderboard

A desktop-based **Quiz Application built with Python, Tkinter, and SQLite**.

The application allows users to register/login, select a quiz category and difficulty level, answer timed multiple-choice questions, view their results, and compete for a position on the leaderboard.

This project was developed as a **Second Semester Python Project**.

---

## ✨ Features

* 🔐 **User Registration & Login**
* 🧠 **Multiple Quiz Categories**

  * Science
  * History
  * Sports
  * General Knowledge
* 🎯 **Easy and Hard Difficulty Levels**
* ⏱️ **Timer for Each Question**
* ✅ Instant Correct/Wrong Answer Feedback
* 📊 Detailed Quiz Results
* 🏆 **Top 10 Leaderboard**
* 💾 SQLite Database for Users, Questions, and Scores
* 🔑 SHA-256 Password Hashing
* 🌐 Optional Question Fetching from the Open Trivia Database (OpenTDB)
* 🖥️ Desktop GUI built entirely with Tkinter

---

## 🛠️ Technologies Used

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| **Python 3** | Core programming language       |
| **Tkinter**  | Graphical User Interface        |
| **SQLite3**  | Local database                  |
| **hashlib**  | Password hashing                |
| **urllib**   | Fetching questions from OpenTDB |
| **JSON**     | Processing API responses        |

The application uses Python's standard library, so no additional Python packages are required.

---

## 📂 Project Structure

```text
Quiz-App/
│
├── main.py
├── fetch_questions.py
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── db_setup.py
│   └── questions_data.py
│
├── screens/
│   ├── __init__.py
│   ├── login_screen.py
│   ├── home_screen.py
│   ├── quiz_setup_screen.py
│   ├── quiz_screen.py
│   ├── result_screen.py
│   └── leaderboard_screen.py
│
└── utils/
    ├── __init__.py
    └── helpers.py
```

---

## 🚀 Getting Started

### Prerequisites

Make sure **Python 3.x** is installed.

Check your Python installation with:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/quiz-app-with-leaderboard.git
```

2. Open the project directory:

```bash
cd quiz-app-with-leaderboard
```

3. Start the application:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

The database is initialized when the application starts.

---

## 🎮 How to Use

1. Launch the application.
2. Register a new account or log in.
3. Select **Start Quiz** from the home screen.
4. Choose a quiz category.
5. Select **Easy** or **Hard** difficulty.
6. Answer the multiple-choice questions before the timer expires.
7. View your score and quiz statistics.
8. Open the **Leaderboard** to compare scores.

---

## 🎯 Quiz Categories

The application currently supports:

* 🔬 Science
* 📜 History
* ⚽ Sports
* 🌍 General Knowledge

---

## ⚡ Difficulty & Scoring

The application provides two difficulty levels:

| Difficulty | Correct Answer | Wrong Answer |
| ---------- | -------------: | -----------: |
| Easy       |            +10 |            0 |
| Hard       |            +10 |           -5 |

This makes Hard mode more challenging because incorrect answers can reduce the player's score.

---

## ⏱️ Quiz System

Each question has a **15-second countdown timer**.

After an answer is selected, the application provides immediate feedback before moving to the next question.

At the end of a quiz, the results screen displays information such as:

* Final Score
* Correct Answers
* Wrong Answers
* Accuracy
* Time Taken

---

## 🏆 Leaderboard

Quiz results are stored in the SQLite database.

The leaderboard displays the **Top 10 scores**, allowing players to compare their performance.

Scores can include information such as:

* Username
* Score
* Category
* Difficulty
* Correct Answers
* Wrong Answers
* Time Taken
* Date

---

## 🌐 Fetching Additional Questions

The project includes:

```text
fetch_questions.py
```

This script can fetch additional multiple-choice questions from the **Open Trivia Database (OpenTDB)**.

It retrieves questions for:

* Science
* History
* Sports
* General Knowledge

with both **Easy** and **Hard** difficulty levels.

Run it using:

```bash
python fetch_questions.py
```

The fetched questions are added to the question bank in:

```text
database/questions_data.py
```

> An internet connection is required when fetching new questions.

---

## 🗄️ Database

The project uses **SQLite** for local data storage.

### Users

Stores registered users and their hashed passwords.

### Questions

Stores quiz questions along with:

* Four answer options
* Correct answer
* Category
* Difficulty

### Scores

Stores completed quiz results used to generate the leaderboard.

The SQLite database file is generated locally and is excluded from Git using `.gitignore`.

---

## 🔐 Password Security

Passwords are not intended to be stored directly as plain text.

The project uses **SHA-256 hashing** before storing password values in the database.

> **Note:** This authentication system is suitable for an educational project. A production application should use a dedicated password-hashing algorithm such as Argon2, bcrypt, or scrypt with unique salts.

---

## 🔄 Application Flow

```text
Login / Register
       │
       ▼
   Home Menu
    │     │
    │     └──────────────► Leaderboard
    │
    ▼
 Quiz Setup
    │
    ▼
 Quiz Session
    │
    ▼
   Results
    │
    └──────────────► Score Saved
```

---

## 🔮 Future Improvements

Possible improvements include:

* More quiz categories
* Additional difficulty levels
* Randomized quiz length
* Improved password security
* User profile and quiz history
* Global/online leaderboard
* Dark/light theme selection
* Sound effects
* Question search and filtering
* Admin panel for managing questions
* Packaging the application as a Windows executable

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit the changes.
5. Push the branch.
6. Open a Pull Request.

---

## 📄 License

This project is intended primarily for educational purposes.

If you want to make it open source, you can add an **MIT License** to the repository.

---

## 👨‍💻 Author

**Shreyansh**

Second Semester Project — 2026

---

⭐ If you found this project useful, consider giving the repository a star!
