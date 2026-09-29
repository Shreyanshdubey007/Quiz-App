"""
home_screen.py  –  Main menu after login.

Shows the logged-in username and three action buttons:
    • Start Quiz
    • View Leaderboard
    • Logout
"""

import tkinter as tk


class HomeScreen(tk.Frame):
    """Home / main-menu screen."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # Centre card
        card = tk.Frame(self, bg="#252545", highlightthickness=1,
                        highlightbackground="#3a3a5c")
        card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=520)

        # Branding
        tk.Label(
            card, text="🧠", font=("Segoe UI", 40),
            bg="#252545", fg="#6c63ff"
        ).pack(pady=(30, 0))

        tk.Label(
            card, text="Quiz App", font=("Segoe UI", 26, "bold"),
            bg="#252545", fg="#ffffff"
        ).pack(pady=(0, 2))

        self.welcome_label = tk.Label(
            card, text="Welcome, Player!", font=("Segoe UI", 12),
            bg="#252545", fg="#7f8c8d"
        )
        self.welcome_label.pack(pady=(0, 25))

        # ── Separator ──
        tk.Frame(card, bg="#6c63ff", height=2).pack(fill="x", padx=80, pady=(0, 20))

        # ── Buttons ──
        buttons = [
            ("▶   Start Quiz",    "#6c63ff", "#7c74ff", lambda: self.app.show_screen("quiz_setup")),
            ("🏆   Leaderboard",  "#00b894", "#00d6a8", lambda: self.app.show_screen("leaderboard")),
            ("🚪   Logout",       "#e74c3c", "#f55c4e", self._logout),
        ]

        for text, bg_color, hover_color, cmd in buttons:
            btn = tk.Button(
                card, text=text, font=("Segoe UI", 14, "bold"),
                bg=bg_color, fg="white", activebackground=hover_color,
                relief="flat", cursor="hand2", width=22, height=2,
                command=cmd
            )
            btn.pack(pady=6)
            btn.bind("<Enter>", lambda e, c=hover_color: e.widget.config(bg=c))
            btn.bind("<Leave>", lambda e, c=bg_color: e.widget.config(bg=c))

    def _logout(self):
        """Clear current user and return to login screen."""
        self.app.current_user = None
        self.app.show_screen("login")

    def on_show(self):
        """Called every time this screen is displayed — refresh username."""
        name = self.app.current_user or "Player"
        self.welcome_label.config(text=f"Welcome, {name}! 👋")
