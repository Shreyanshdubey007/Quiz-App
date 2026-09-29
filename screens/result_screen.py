"""
result_screen.py  –  Results screen shown after completing a quiz.

Displays:
    • Final score
    • Number of correct / wrong answers
    • Accuracy percentage
    • Total time taken

Action buttons:
    • Save Score   – saves to the leaderboard database
    • Play Again   – go back to quiz setup
    • Go Home      – return to main menu
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database.db_setup import save_score
from utils.helpers import format_time


class ResultScreen(tk.Frame):
    """Post-quiz results summary screen."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._score_saved = False
        self._build_ui()

    # ──────────────────── UI CONSTRUCTION ────────────────────
    def _build_ui(self):
        # Title
        tk.Label(
            self, text="📊", font=("Segoe UI", 36),
            bg="#1a1a2e", fg="#6c63ff"
        ).pack(pady=(20, 0))

        tk.Label(
            self, text="Quiz Results", font=("Segoe UI", 24, "bold"),
            bg="#1a1a2e", fg="#ffffff"
        ).pack(pady=(0, 5))

        # ── Score highlight ──
        score_frame = tk.Frame(self, bg="#252545", highlightthickness=1,
                               highlightbackground="#6c63ff")
        score_frame.pack(padx=120, pady=10, fill="x")

        self.score_label = tk.Label(
            score_frame, text="0", font=("Segoe UI", 42, "bold"),
            bg="#252545", fg="#6c63ff"
        )
        self.score_label.pack(pady=(12, 0))

        tk.Label(
            score_frame, text="POINTS", font=("Segoe UI", 10, "bold"),
            bg="#252545", fg="#7f8c8d"
        ).pack(pady=(0, 10))

        # ── Stats grid ──
        stats_card = tk.Frame(self, bg="#252545", highlightthickness=1,
                              highlightbackground="#3a3a5c")
        stats_card.pack(padx=80, pady=8, fill="x")

        stats_inner = tk.Frame(stats_card, bg="#252545")
        stats_inner.pack(padx=20, pady=15)

        self.correct_label = self._stat_row(stats_inner, "✅  Correct", "0", "#27ae60", 0)
        self.wrong_label = self._stat_row(stats_inner, "❌  Wrong", "0", "#e74c3c", 1)
        self.accuracy_label = self._stat_row(stats_inner, "🎯  Accuracy", "0%", "#f39c12", 2)
        self.time_label = self._stat_row(stats_inner, "⏱   Time Taken", "00:00", "#3498db", 3)
        self.category_label = self._stat_row(stats_inner, "📂  Category", "-", "#b0b0b0", 4)
        self.difficulty_label = self._stat_row(stats_inner, "⚡  Difficulty", "-", "#b0b0b0", 5)

        stats_inner.columnconfigure(0, weight=1, minsize=180)
        stats_inner.columnconfigure(1, weight=1, minsize=120)

        # ── Action buttons ──
        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(pady=(15, 20))

        buttons = [
            ("save_btn", "💾  Save Score",  "#6c63ff", "#7c74ff", self._save_score),
            (None,       "🔄  Play Again",  "#00b894", "#00d6a8", lambda: self.app.show_screen("quiz_setup")),
            (None,       "🏠  Go Home",     "#3a3a55", "#4a4a6a", lambda: self.app.show_screen("home")),
        ]

        for attr, text, bg_c, hover_c, cmd in buttons:
            btn = tk.Button(
                btn_frame, text=text, font=("Segoe UI", 11, "bold"),
                bg=bg_c, fg="white", relief="flat", width=16, height=1,
                cursor="hand2", activebackground=hover_c,
                command=cmd
            )
            btn.pack(side="left", padx=6, ipady=4)
            btn.bind("<Enter>", lambda e, c=hover_c: e.widget.config(bg=c))
            btn.bind("<Leave>", lambda e, c=bg_c: e.widget.config(bg=c))

            if attr == "save_btn":
                self.save_btn = btn
                self._save_bg = bg_c

    def _stat_row(self, parent, label_text, value_text, color, row):
        """Create a label + value row inside the stats grid."""
        tk.Label(
            parent, text=label_text, font=("Segoe UI", 11),
            bg="#252545", fg="#b0b0b0", anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=(10, 10), pady=4)

        val_label = tk.Label(
            parent, text=value_text, font=("Segoe UI", 13, "bold"),
            bg="#252545", fg=color, anchor="e"
        )
        val_label.grid(row=row, column=1, sticky="e", padx=(10, 10), pady=4)

        return val_label

    # ──────────────────── SCREEN LIFECYCLE ────────────────────
    def on_show(self):
        """Populate result data when screen is displayed."""
        results = self.app.quiz_results
        if not results:
            return

        score = results["score"]
        correct = results["correct"]
        wrong = results["wrong"]
        total = results["total"]
        time_taken = results["time_taken"]
        category = results["category"]
        difficulty = results["difficulty"]

        accuracy = (correct / total * 100) if total > 0 else 0

        self.score_label.config(text=str(score))
        self.correct_label.config(text=str(correct))
        self.wrong_label.config(text=str(wrong))
        self.accuracy_label.config(text=f"{accuracy:.1f}%")
        self.time_label.config(text=format_time(time_taken))
        self.category_label.config(text=category)
        self.difficulty_label.config(text=difficulty)

        # Reset save button state
        self._score_saved = False
        self.save_btn.config(state="normal", text="💾  Save Score", bg="#6c63ff")

    # ──────────────────── SAVE SCORE ────────────────────
    def _save_score(self):
        """Save the current quiz score to the leaderboard database."""
        if self._score_saved:
            return

        results = self.app.quiz_results
        username = self.app.current_user

        save_score(
            username=username,
            score=results["score"],
            category=results["category"],
            difficulty=results["difficulty"],
            total_questions=results["total"],
            correct=results["correct"],
            wrong=results["wrong"],
            time_taken=results["time_taken"],
            date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        self._score_saved = True
        self.save_btn.config(state="disabled", text="✅  Saved!", bg="#3a3a55")
        messagebox.showinfo("Saved", "Your score has been saved to the leaderboard!")
