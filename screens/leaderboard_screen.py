"""
leaderboard_screen.py  –  Leaderboard display.

Fetches the top 10 scores from the database and presents them in
a ranked table using tkinter Treeview widget.

Columns: Rank, Username, Score, Category, Difficulty, Date
"""

import tkinter as tk
from tkinter import ttk
from database.db_setup import fetch_leaderboard


class LeaderboardScreen(tk.Frame):
    """Leaderboard screen displaying top 10 scores."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()

    # ──────────────────── UI CONSTRUCTION ────────────────────
    def _build_ui(self):
        # Title
        tk.Label(
            self, text="🏆", font=("Segoe UI", 36),
            bg="#1a1a2e", fg="#f1c40f"
        ).pack(pady=(20, 0))

        tk.Label(
            self, text="Leaderboard", font=("Segoe UI", 24, "bold"),
            bg="#1a1a2e", fg="#ffffff"
        ).pack(pady=(0, 2))

        tk.Label(
            self, text="Top 10 Scores", font=("Segoe UI", 11),
            bg="#1a1a2e", fg="#7f8c8d"
        ).pack(pady=(0, 12))

        # ── Separator ──
        tk.Frame(self, bg="#f1c40f", height=2).pack(fill="x", padx=180, pady=(0, 12))

        # ── Treeview table ──
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Leader.Treeview",
                        background="#252545",
                        foreground="#f1f1f1",
                        fieldbackground="#252545",
                        font=("Segoe UI", 11),
                        rowheight=34,
                        borderwidth=0)
        style.configure("Leader.Treeview.Heading",
                        background="#1a1a2e",
                        foreground="#6c63ff",
                        font=("Segoe UI", 11, "bold"),
                        relief="flat",
                        borderwidth=0)
        style.map("Leader.Treeview",
                  background=[("selected", "#6c63ff")])
        style.map("Leader.Treeview.Heading",
                  background=[("active", "#252545")])

        columns = ("rank", "username", "score", "category", "difficulty", "date")

        tree_frame = tk.Frame(self, bg="#1a1a2e")
        tree_frame.pack(fill="both", expand=True, padx=30, pady=5)

        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings",
            style="Leader.Treeview", height=10
        )

        self.tree.heading("rank",       text="#")
        self.tree.heading("username",   text="Player")
        self.tree.heading("score",      text="Score")
        self.tree.heading("category",   text="Category")
        self.tree.heading("difficulty", text="Difficulty")
        self.tree.heading("date",       text="Date")

        self.tree.column("rank",       width=40,  anchor="center")
        self.tree.column("username",   width=120, anchor="center")
        self.tree.column("score",      width=70,  anchor="center")
        self.tree.column("category",   width=130, anchor="center")
        self.tree.column("difficulty", width=80,  anchor="center")
        self.tree.column("date",       width=130, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ── Empty state label ──
        self.empty_label = tk.Label(
            self, text="No scores recorded yet.\nPlay a quiz and save your score!",
            font=("Segoe UI", 13), bg="#1a1a2e", fg="#555555", justify="center"
        )

        # ── Back button ──
        back_btn = tk.Button(
            self, text="◀  Back to Home", font=("Segoe UI", 12, "bold"),
            bg="#3a3a55", fg="white", relief="flat", width=18,
            cursor="hand2", activebackground="#4a4a6a",
            command=lambda: self.app.show_screen("home")
        )
        back_btn.pack(pady=(8, 20), ipady=5)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#4a4a6a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#3a3a55"))

    # ──────────────────── SCREEN LIFECYCLE ────────────────────
    def on_show(self):
        """Refresh leaderboard data every time the screen is shown."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = fetch_leaderboard(limit=10)

        if not data:
            self.empty_label.pack(pady=10)
        else:
            self.empty_label.pack_forget()
            for row in data:
                tag = ""
                if row[0] == 1:
                    tag = "gold"
                elif row[0] == 2:
                    tag = "silver"
                elif row[0] == 3:
                    tag = "bronze"

                self.tree.insert("", "end", values=row, tags=(tag,))

            self.tree.tag_configure("gold",   foreground="#FFD700", font=("Segoe UI", 11, "bold"))
            self.tree.tag_configure("silver", foreground="#C0C0C0", font=("Segoe UI", 11, "bold"))
            self.tree.tag_configure("bronze", foreground="#CD7F32", font=("Segoe UI", 11, "bold"))
