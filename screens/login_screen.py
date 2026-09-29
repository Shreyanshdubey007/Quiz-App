"""
login_screen.py  –  Login and Register screen.

Provides two tabs (Login / Register) inside a styled frame.
Uses SHA-256 hashing for passwords via utils.helpers.
"""

import tkinter as tk
from tkinter import messagebox
from utils.helpers import hash_password, validate_username, validate_password
from database.db_setup import register_user, authenticate_user


class LoginScreen(tk.Frame):
    """Login / Register screen shown on app launch."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._mode = "login"
        self._build_ui()

    # ──────────────────── UI CONSTRUCTION ────────────────────
    def _build_ui(self):
        # Centre card with rounded-feel styling
        card = tk.Frame(self, bg="#252545", bd=0, highlightthickness=1,
                        highlightbackground="#3a3a5c")
        card.place(relx=0.5, rely=0.5, anchor="center", width=430, height=500)

        # ── App branding ──
        tk.Label(
            card, text="🧠", font=("Segoe UI", 36),
            bg="#252545", fg="#6c63ff"
        ).pack(pady=(25, 0))

        tk.Label(
            card, text="Quiz App", font=("Segoe UI", 22, "bold"),
            bg="#252545", fg="#ffffff"
        ).pack(pady=(0, 2))

        self.subtitle_label = tk.Label(
            card, text="Login to continue", font=("Segoe UI", 10),
            bg="#252545", fg="#7f8c8d"
        )
        self.subtitle_label.pack(pady=(0, 18))

        # ── Tab buttons ──
        tab_frame = tk.Frame(card, bg="#252545")
        tab_frame.pack(pady=(0, 15))

        self.login_tab_btn = tk.Button(
            tab_frame, text="Login", font=("Segoe UI", 11, "bold"),
            bg="#6c63ff", fg="white", relief="flat", width=14, height=1,
            cursor="hand2", activebackground="#7c74ff",
            command=lambda: self._switch_mode("login")
        )
        self.login_tab_btn.pack(side="left", padx=4)

        self.register_tab_btn = tk.Button(
            tab_frame, text="Register", font=("Segoe UI", 11),
            bg="#3a3a55", fg="#bbbbbb", relief="flat", width=14, height=1,
            cursor="hand2", activebackground="#4a4a6a",
            command=lambda: self._switch_mode("register")
        )
        self.register_tab_btn.pack(side="left", padx=4)

        # ── Username field ──
        tk.Label(
            card, text="👤  Username", font=("Segoe UI", 10, "bold"),
            bg="#252545", fg="#b0b0b0", anchor="w"
        ).pack(fill="x", padx=50)

        self.username_entry = tk.Entry(
            card, font=("Segoe UI", 12), bg="#1a1a2e", fg="white",
            insertbackground="#6c63ff", relief="flat", bd=8,
            highlightthickness=1, highlightcolor="#6c63ff",
            highlightbackground="#3a3a5c"
        )
        self.username_entry.pack(fill="x", padx=50, pady=(2, 10))

        # ── Password field ──
        tk.Label(
            card, text="🔒  Password", font=("Segoe UI", 10, "bold"),
            bg="#252545", fg="#b0b0b0", anchor="w"
        ).pack(fill="x", padx=50)

        self.password_entry = tk.Entry(
            card, font=("Segoe UI", 12), bg="#1a1a2e", fg="white",
            insertbackground="#6c63ff", relief="flat", bd=8, show="●",
            highlightthickness=1, highlightcolor="#6c63ff",
            highlightbackground="#3a3a5c"
        )
        self.password_entry.pack(fill="x", padx=50, pady=(2, 10))

        # ── Confirm Password (visible only in Register mode) ──
        self.confirm_label = tk.Label(
            card, text="🔒  Confirm Password", font=("Segoe UI", 10, "bold"),
            bg="#252545", fg="#b0b0b0", anchor="w"
        )
        self.confirm_entry = tk.Entry(
            card, font=("Segoe UI", 12), bg="#1a1a2e", fg="white",
            insertbackground="#6c63ff", relief="flat", bd=8, show="●",
            highlightthickness=1, highlightcolor="#6c63ff",
            highlightbackground="#3a3a5c"
        )
        # Hidden by default (login mode)

        # ── Action button ──
        self.action_btn = tk.Button(
            card, text="Login  →", font=("Segoe UI", 13, "bold"),
            bg="#6c63ff", fg="white", activebackground="#7c74ff",
            relief="flat", cursor="hand2", height=1,
            command=self._on_action
        )
        self.action_btn.pack(fill="x", padx=50, pady=(12, 8))

        # Hover effect on action button
        self.action_btn.bind("<Enter>", lambda e: self.action_btn.config(bg="#7c74ff"))
        self.action_btn.bind("<Leave>", lambda e: self.action_btn.config(bg="#6c63ff"))

        # ── Status label ──
        self.status_label = tk.Label(
            card, text="", font=("Segoe UI", 9),
            bg="#252545", fg="#ff6b6b"
        )
        self.status_label.pack()

        # Bind Enter key for smooth field navigation
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda e: (
            self.confirm_entry.focus_set() if self._mode == "register"
            else self._on_action()
        ))
        self.confirm_entry.bind("<Return>", lambda e: self._on_action())

    # ──────────────────── MODE SWITCHING ────────────────────
    def _switch_mode(self, mode):
        self._mode = mode
        self.status_label.config(text="")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")

        if mode == "login":
            self.subtitle_label.config(text="Login to continue")
            self.login_tab_btn.config(bg="#6c63ff", fg="white", font=("Segoe UI", 11, "bold"))
            self.register_tab_btn.config(bg="#3a3a55", fg="#bbbbbb", font=("Segoe UI", 11))
            self.confirm_label.pack_forget()
            self.confirm_entry.pack_forget()
            self.action_btn.config(text="Login  →")
        else:
            self.subtitle_label.config(text="Create a new account")
            self.register_tab_btn.config(bg="#6c63ff", fg="white", font=("Segoe UI", 11, "bold"))
            self.login_tab_btn.config(bg="#3a3a55", fg="#bbbbbb", font=("Segoe UI", 11))
            # Show confirm password field above the action button
            self.action_btn.pack_forget()
            self.status_label.pack_forget()
            self.confirm_label.pack(fill="x", padx=50)
            self.confirm_entry.pack(fill="x", padx=50, pady=(2, 10))
            self.action_btn.pack(fill="x", padx=50, pady=(12, 8))
            self.action_btn.config(text="Register  →")
            self.status_label.pack()

        self.username_entry.focus_set()

    # ──────────────────── ACTION HANDLER ────────────────────
    def _on_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if self._mode == "login":
            if not username or not password:
                self.status_label.config(text="Please enter both username and password.", fg="#ff6b6b")
                return
                
            hashed = hash_password(password)
            if authenticate_user(username, hashed):
                self.status_label.config(text="")
                self.app.current_user = username
                self.app.show_screen("home")
            else:
                self.status_label.config(text="Incorrect username or password.", fg="#ff6b6b")
                
        else:   # register mode
            # Validate username
            valid, msg = validate_username(username)
            if not valid:
                self.status_label.config(text=msg, fg="#ff6b6b")
                return

            # Validate password
            valid, msg = validate_password(password)
            if not valid:
                self.status_label.config(text=msg, fg="#ff6b6b")
                return

            confirm = self.confirm_entry.get()
            if password != confirm:
                self.status_label.config(text="Passwords do not match.", fg="#ff6b6b")
                return

            hashed = hash_password(password)
            success = register_user(username, hashed)
            if success:
                messagebox.showinfo("Success", f"Account created for '{username}'!\nYou can now login.")
                self._switch_mode("login")
            else:
                self.status_label.config(text="Username already taken.", fg="#ff6b6b")
