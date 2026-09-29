"""
main.py  –  Entry point for the Quiz App.

This module creates the main Tkinter window and manages navigation
between all screens using a frame-swapping pattern.

Run this file to start the application:
    python main.py
"""

import tkinter as tk
from database.db_setup import initialise_database
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.quiz_setup_screen import QuizSetupScreen
from screens.quiz_screen import QuizScreen
from screens.result_screen import ResultScreen
from screens.leaderboard_screen import LeaderboardScreen


class App:
    """
    Main application controller.

    Manages the root Tkinter window and handles screen navigation.
    Each screen is a tk.Frame stored in self.screens dict.
    """

    def __init__(self):
        # Initialise the SQLite database (creates tables + seeds questions)
        initialise_database()

        # ── Root window setup ──
        self.root = tk.Tk()
        self.root.title("Quiz App with Leaderboard")
        self.root.geometry("700x600")
        self.root.minsize(650, 550)
        self.root.configure(bg="#1e1e2f")

        # Try to set window icon (optional, won't crash if icon is missing)
        try:
            self.root.iconbitmap("icon.ico")
        except tk.TclError:
            pass

        # ── Shared application state ──
        self.current_user = None        # username of the logged-in user
        self.quiz_category = None       # selected category for the quiz
        self.quiz_difficulty = None      # selected difficulty for the quiz
        self.quiz_results = None        # dict with results after a quiz

        # ── Container frame (all screens are packed here) ──
        self.container = tk.Frame(self.root, bg="#1e1e2f")
        self.container.pack(fill="both", expand=True)

        # ── Create all screens ──
        self.screens = {}
        self._current_screen_name = None

        screen_classes = {
            "login":      LoginScreen,
            "home":       HomeScreen,
            "quiz_setup": QuizSetupScreen,
            "quiz":       QuizScreen,
            "result":     ResultScreen,
            "leaderboard": LeaderboardScreen,
        }

        for name, ScreenClass in screen_classes.items():
            screen = ScreenClass(self.container, self)
            self.screens[name] = screen

        # Show the login screen first
        self.show_screen("login")

    # ──────────────────── NAVIGATION ────────────────────
    def show_screen(self, screen_name: str):
        """
        Switch to the specified screen.
        Hides the current screen and shows the new one.
        Calls on_hide() / on_show() lifecycle methods if they exist.
        """
        # Hide current screen
        if self._current_screen_name:
            current = self.screens[self._current_screen_name]
            if hasattr(current, "on_hide"):
                current.on_hide()
            current.pack_forget()

        # Show new screen
        new_screen = self.screens[screen_name]
        new_screen.pack(fill="both", expand=True)

        if hasattr(new_screen, "on_show"):
            new_screen.on_show()

        self._current_screen_name = screen_name

    # ──────────────────── RUN ────────────────────
    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()


# ──────────────────── ENTRY POINT ────────────────────
if __name__ == "__main__":
    app = App()
    app.run()
