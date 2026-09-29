"""
quiz_setup_screen.py  –  Category & Difficulty selection.

Lets the user pick:
    • Category   – Science, History, Sports, General Knowledge
    • Difficulty  – Easy, Hard

Then starts the quiz session with the selected filters.
"""

import tkinter as tk
from utils.helpers import CATEGORIES, DIFFICULTIES


class QuizSetupScreen(tk.Frame):
    """Screen for selecting quiz category and difficulty before starting."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.cat_buttons = []       # list of (value, frame, indicator_label)
        self.diff_buttons = []
        self._build_ui()

    def _build_ui(self):
        # Top padding
        tk.Frame(self, bg="#1a1a2e", height=25).pack()

        # Title area
        title_frame = tk.Frame(self, bg="#1a1a2e")
        title_frame.pack(pady=(10, 0))

        tk.Label(
            title_frame, text="⚙", font=("Segoe UI", 30),
            bg="#1a1a2e", fg="#6c63ff"
        ).pack()
        tk.Label(
            title_frame, text="Quiz Setup", font=("Segoe UI", 24, "bold"),
            bg="#1a1a2e", fg="#ffffff"
        ).pack()
        tk.Label(
            title_frame, text="Pick your arena and challenge level",
            font=("Segoe UI", 11), bg="#1a1a2e", fg="#7f8c8d"
        ).pack(pady=(2, 0))

        # ── Separator line ──
        tk.Frame(self, bg="#6c63ff", height=2).pack(fill="x", padx=180, pady=(15, 15))

        # ── Main content area ──
        content = tk.Frame(self, bg="#1a1a2e")
        content.pack(fill="x", padx=80)

        # ── Category section ──
        tk.Label(
            content, text="📂  Category", font=("Segoe UI", 13, "bold"),
            bg="#1a1a2e", fg="#e0e0e0"
        ).pack(anchor="w", pady=(5, 8))

        self.category_var = tk.StringVar(value=CATEGORIES[0])
        cat_emojis = {"Science": "🔬", "History": "📜", "Sports": "⚽", "General Knowledge": "💡"}

        cat_grid = tk.Frame(content, bg="#1a1a2e")
        cat_grid.pack(fill="x", pady=(0, 10))

        for cat in CATEGORIES:
            emoji = cat_emojis.get(cat, "")
            self._create_option_row(
                cat_grid, cat, emoji, self.category_var, self.cat_buttons
            )

        # ── Difficulty section ──
        tk.Label(
            content, text="⚡  Difficulty", font=("Segoe UI", 13, "bold"),
            bg="#1a1a2e", fg="#e0e0e0"
        ).pack(anchor="w", pady=(15, 8))

        self.difficulty_var = tk.StringVar(value=DIFFICULTIES[0])
        diff_info = {
            "Easy": ("🟢", "+10 correct,  0 wrong"),
            "Hard": ("🔴", "+10 correct, −5 wrong")
        }

        diff_grid = tk.Frame(content, bg="#1a1a2e")
        diff_grid.pack(fill="x", pady=(0, 5))

        for diff in DIFFICULTIES:
            emoji, desc = diff_info[diff]
            display = f"{diff}   ({desc})"
            self._create_option_row(
                diff_grid, diff, emoji, self.difficulty_var, self.diff_buttons,
                display_text=display
            )

        # ── Buttons at the bottom ──
        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(pady=(25, 30))

        back_btn = tk.Button(
            btn_frame, text="◀  Back", font=("Segoe UI", 12, "bold"),
            bg="#3a3a55", fg="white", relief="flat", width=12, height=2,
            cursor="hand2", activebackground="#4a4a6a",
            command=lambda: self.app.show_screen("home")
        )
        back_btn.pack(side="left", padx=10)

        start_btn = tk.Button(
            btn_frame, text="Start Quiz  ▶", font=("Segoe UI", 13, "bold"),
            bg="#6c63ff", fg="white", activebackground="#5a54e0",
            relief="flat", width=16, height=2, cursor="hand2",
            command=self._start_quiz
        )
        start_btn.pack(side="left", padx=10)

        self._add_hover(back_btn, "#4a4a6a", "#3a3a55")
        self._add_hover(start_btn, "#7c74ff", "#6c63ff")

        # Initial highlight
        self._refresh_selection(self.category_var, self.cat_buttons)
        self._refresh_selection(self.difficulty_var, self.diff_buttons)

    # ──────────────────── CUSTOM RADIO ROW ────────────────────
    def _create_option_row(self, parent, value, emoji, var, btn_list,
                           display_text=None):
        """
        Create a custom radio-button row with a visible ○/● indicator.
        White circle (○) when unselected → Green filled circle (●) when selected.
        """
        text = display_text or value

        row = tk.Frame(parent, bg="#252545", cursor="hand2")
        row.pack(fill="x", pady=3, ipady=6)

        # Green accent bar on the left (hidden by default)
        accent = tk.Frame(row, bg="#252545", width=4)
        accent.pack(side="left", fill="y")

        # Circle indicator
        indicator = tk.Label(
            row, text="○", font=("Segoe UI", 14),
            bg="#252545", fg="white", padx=10
        )
        indicator.pack(side="left")

        # Emoji + text
        label = tk.Label(
            row, text=f" {emoji}  {text}", font=("Segoe UI", 12),
            bg="#252545", fg="#e0e0e0", anchor="w"
        )
        label.pack(side="left", fill="x", expand=True)

        btn_list.append((value, row, indicator, accent, label))

        # Click handler — bind to all child widgets too
        def on_click(e=None):
            var.set(value)
            self._refresh_selection(var, btn_list)

        for widget in (row, indicator, label):
            widget.bind("<Button-1>", on_click)

    def _refresh_selection(self, var, btn_list):
        """Update all rows in a group to reflect the current selection."""
        selected = var.get()
        for val, row, indicator, accent, label in btn_list:
            if val == selected:
                indicator.config(text="●", fg="#2ecc71")       # green filled
                accent.config(bg="#2ecc71")                     # green left bar
                row.config(bg="#2a2a48")
                indicator.config(bg="#2a2a48")
                label.config(bg="#2a2a48", fg="#ffffff")
            else:
                indicator.config(text="○", fg="white")          # white hollow
                accent.config(bg="#252545")                      # hidden
                row.config(bg="#252545")
                indicator.config(bg="#252545")
                label.config(bg="#252545", fg="#e0e0e0")

    # ──────────────────── HELPERS ────────────────────
    def _add_hover(self, widget, hover_color, normal_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))

    def _start_quiz(self):
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()

        self.app.quiz_category = category
        self.app.quiz_difficulty = difficulty
        self.app.show_screen("quiz")

