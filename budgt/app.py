
import sys
from .database import init_db
from .tui import ExpenseApp
from . import __version__

def main():
    """Main entry point for the Budgt.sh application."""
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--version', '-v']:
            print(f"Budgt.sh v{__version__}")
            return
        elif sys.argv[1] in ['--help', '-h']:
            print(f"""Budgt.sh v{__version__}
A modern Terminal User Interface (TUI) application for tracking personal expenses and budgeting.

Usage:
    budgt              Start the application
    budgt --version    Show version information
    budgt --help       Show this help message

Keyboard Shortcuts (when running):
    a         Add new account
    t         Add new transaction  
    Shift+T   Transfer money between accounts
    Ctrl+T    Toggle theme
    q         Quit application

For more information, visit: https://github.com/yourusername/budgt.sh
""")
            return
    
    # Initialize database and run app
    init_db()
    app = ExpenseApp()
    app.run()

if __name__ == "__main__":
    main()

