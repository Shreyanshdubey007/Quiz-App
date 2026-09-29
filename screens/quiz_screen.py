"""
quiz_screen.py  –  The actual quiz session.

Features:
    • Displays one question at a time with 4 option buttons
    • 15-second countdown timer per question (using Tkinter after())
    • Highlights correct answer in green, wrong in red
    • Awards +10 for correct, 0 for wrong (Easy), -5 for wrong (Hard)
    • Tracks score, correct/wrong counts, and total time
    • Auto-advances to next question after a short delay
"""

import tkinter as tk
import time
from database.db_setup import fetch_questions
from utils.helpers import (
    POINTS_CORRECT, POINTS_WRONG_EASY, POINTS_WRONG_HARD,
    TIME_PER_QUESTION, QUESTIONS_PER_QUIZ
)


class QuizScreen(tk.Frame):
    """Interactive quiz session screen."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._timer_id = None
        self._build_ui()

    # ──────────────────── UI CONSTRUCTION ────────────────────
    def _build_ui(self):
        # Top bar
        top_bar = tk.Frame(self, bg="#252545", pady=8)
        top_bar.pack(fill="x", padx=25, pady=(15, 0))

        self.progress_label = tk.Label(
            top_bar, text="Question 1 / 10", font=("Segoe UI", 11, "bold"),
            bg="#252545", fg="#7f8c8d"
        )
        self.progress_label.pack(side="left", padx=10)

        self.score_label = tk.Label(
            top_bar, text="Score: 0", font=("Segoe UI", 12, "bold"),
            bg="#252545", fg="#6c63ff"
        )
        self.score_label.pack(side="right", padx=15)

        # Category & Difficulty badge
        self.info_label = tk.Label(
            self, text="Science  •  Easy", font=("Segoe UI", 10),
            bg="#1a1a2e", fg="#555555"
        )
        self.info_label.pack(pady=(8, 5))

        # ── Progress bar ──
        progress_bg = tk.Frame(self, bg="#3a3a55", height=4)
        progress_bg.pack(fill="x", padx=25, pady=(0, 10))
        progress_bg.pack_propagate(False)

        self.progress_bar = tk.Frame(progress_bg, bg="#6c63ff", height=4)
        self.progress_bar.place(x=0, y=0, relwidth=0.1, relheight=1.0)

        # ── Timer bar (above question, with spacing) ──
        timer_row = tk.Frame(self, bg="#1a1a2e")
        timer_row.pack(fill="x", padx=25, pady=(5, 12))

        self.timer_seconds_label = tk.Label(
            timer_row, text="15s", font=("Segoe UI", 11, "bold"),
            bg="#1a1a2e", fg="#7f8c8d"
        )
        self.timer_seconds_label.pack(side="right", padx=(5, 0))

        timer_bar_frame = tk.Frame(timer_row, bg="#3a3a55", height=10)
        timer_bar_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        timer_bar_frame.pack_propagate(False)

        self.timer_bar = tk.Frame(timer_bar_frame, bg="#2ecc71", height=10)
        self.timer_bar.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        # Question card
        q_card = tk.Frame(self, bg="#252545", highlightthickness=1,
                          highlightbackground="#3a3a5c")
        q_card.pack(fill="x", padx=25, pady=5)

        self.question_label = tk.Label(
            q_card, text="Question goes here?",
            font=("Segoe UI", 15, "bold"), bg="#252545", fg="#f1f1f1",
            wraplength=580, justify="center"
        )
        self.question_label.pack(padx=25, pady=28)

        # Option buttons
        self.option_buttons = []
        options_frame = tk.Frame(self, bg="#1a1a2e")
        options_frame.pack(fill="x", padx=40, pady=(8, 5))

        option_letters = ["A", "B", "C", "D"]
        for i in range(4):
            btn = tk.Button(
                options_frame, text=f"  {option_letters[i]}.  Option {i+1}",
                font=("Segoe UI", 12), bg="#252545", fg="white",
                activebackground="#3a3a55", relief="flat",
                cursor="hand2", height=2, anchor="w", padx=20,
                highlightthickness=1, highlightbackground="#3a3a5c",
                command=lambda idx=i: self._on_answer(idx)
            )
            btn.pack(fill="x", pady=3)
            # Hover effects
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#3a3a55") if e.widget["state"] != "disabled" else None)
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#252545") if e.widget["state"] != "disabled" else None)
            self.option_buttons.append(btn)

        # Feedback label
        self.feedback_label = tk.Label(
            self, text="", font=("Segoe UI", 13, "bold"),
            bg="#1a1a2e", fg="#f1f1f1"
        )
        self.feedback_label.pack(pady=(8, 0))

    # ──────────────────── QUIZ SESSION MANAGEMENT ────────────────────
    def on_show(self):
        """Called when this screen is displayed — start a fresh quiz."""
        self.category = self.app.quiz_category
        self.difficulty = self.app.quiz_difficulty

        self.info_label.config(text=f"{self.category}  •  {self.difficulty}")

        # Fetch questions from DB
        self.questions = fetch_questions(
            self.category, self.difficulty, QUESTIONS_PER_QUIZ
        )

        if not self.questions:
            self.question_label.config(text="No questions available for this selection!")
            for btn in self.option_buttons:
                btn.pack_forget()
            return

        # Reset state
        self.current_index = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.time_remaining = TIME_PER_QUESTION
        self.start_time = time.time()
        self.answered = False
        self._timer_id = None

        # Make sure option buttons are visible
        for btn in self.option_buttons:
            btn.pack(fill="x", pady=3)

        self._show_question()

    def _show_question(self):
        """Display the current question and its options."""
        self.answered = False
        self.feedback_label.config(text="")

        q = self.questions[self.current_index]
        # q = (id, question, opt_a, opt_b, opt_c, opt_d, correct_option)

        total = len(self.questions)
        self.progress_label.config(
            text=f"Question {self.current_index + 1} / {total}"
        )
        self.score_label.config(text=f"Score: {self.score}")
        self.question_label.config(text=q[1])

        # Update progress bar
        progress_pct = (self.current_index) / total
        self.progress_bar.place(x=0, y=0, relwidth=max(progress_pct, 0.02), relheight=1.0)

        # Set option texts
        option_labels = ["A", "B", "C", "D"]
        for i, btn in enumerate(self.option_buttons):
            btn.config(
                text=f"  {option_labels[i]}.   {q[2 + i]}",
                bg="#252545", fg="white", state="normal",
                highlightbackground="#3a3a5c"
            )

        # Start countdown timer
        self.time_remaining = TIME_PER_QUESTION
        self._update_timer()

    def _update_timer(self):
        """Tick the countdown timer every second."""
        if self.answered:
            return

        # Update seconds counter
        self.timer_seconds_label.config(text=f"{self.time_remaining}s")

        # Update timer bar width (shrinks as time decreases)
        fraction = self.time_remaining / TIME_PER_QUESTION
        bar_color = "#e74c3c" if self.time_remaining <= 5 else "#2ecc71"
        self.timer_bar.config(bg=bar_color)
        self.timer_bar.place(x=0, y=0, relwidth=max(fraction, 0.0), relheight=1.0)

        # Also tint the seconds label
        self.timer_seconds_label.config(
            fg="#e74c3c" if self.time_remaining <= 5 else "#7f8c8d"
        )

        if self.time_remaining <= 0:
            self._time_up()
            return

        self.time_remaining -= 1
        self._timer_id = self.after(1000, self._update_timer)

    def _time_up(self):
        """Handle case when timer runs out."""
        self.answered = True
        q = self.questions[self.current_index]
        correct_idx = "ABCD".index(q[6])

        self.option_buttons[correct_idx].config(bg="#27ae60", fg="white",
                                                 highlightbackground="#27ae60")

        for btn in self.option_buttons:
            btn.config(state="disabled")

        self.wrong_count += 1

        if self.difficulty == "Hard":
            self.score += POINTS_WRONG_HARD

        self.feedback_label.config(
            text=f"⏰  Time's up!  Correct answer was: {q[6]}",
            fg="#e74c3c"
        )
        self.score_label.config(text=f"Score: {self.score}")

        self.after(1500, self._next_question)

    def _on_answer(self, selected_index):
        """Handle when user clicks an option button."""
        if self.answered:
            return
        self.answered = True

        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

        q = self.questions[self.current_index]
        correct_letter = q[6]
        correct_idx = "ABCD".index(correct_letter)

        for btn in self.option_buttons:
            btn.config(state="disabled")

        if selected_index == correct_idx:
            self.option_buttons[selected_index].config(
                bg="#27ae60", fg="white", highlightbackground="#27ae60"
            )
            self.score += POINTS_CORRECT
            self.correct_count += 1
            self.feedback_label.config(text="✅  Correct!  Well done!", fg="#27ae60")
        else:
            self.option_buttons[selected_index].config(
                bg="#e74c3c", fg="white", highlightbackground="#e74c3c"
            )
            self.option_buttons[correct_idx].config(
                bg="#27ae60", fg="white", highlightbackground="#27ae60"
            )
            self.wrong_count += 1

            if self.difficulty == "Hard":
                self.score += POINTS_WRONG_HARD
            else:
                self.score += POINTS_WRONG_EASY

            self.feedback_label.config(
                text=f"❌  Wrong!  Correct answer: {correct_letter}",
                fg="#e74c3c"
            )

        self.score_label.config(text=f"Score: {self.score}")
        self.after(1500, self._next_question)

    def _next_question(self):
        """Advance to the next question or show results."""
        self.current_index += 1
        if self.current_index < len(self.questions):
            self._show_question()
        else:
            # Update progress bar to 100%
            self.progress_bar.place(x=0, y=0, relwidth=1.0, relheight=1.0)

            total_time = int(time.time() - self.start_time)
            self.app.quiz_results = {
                "score": self.score,
                "correct": self.correct_count,
                "wrong": self.wrong_count,
                "total": len(self.questions),
                "time_taken": total_time,
                "category": self.category,
                "difficulty": self.difficulty,
            }
            self.app.show_screen("result")

    def on_hide(self):
        """Called when navigating away — stop any pending timer."""
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
