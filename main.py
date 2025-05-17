import os
import sys

def get_resource_path():
    # Get the path to the directory containing the script/executable
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # If the application is run from a Python interpreter
        return os.path.dirname(os.path.abspath(__file__))

# Add project root to Python path for absolute imports
project_root = get_resource_path()
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import logging
from utils.themes.colors import ThemeColors

# Configure logging to suppress info messages
logging.basicConfig(level=logging.WARNING)

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide dark theme immediately
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {ThemeColors.BACKGROUND};
            color: {ThemeColors.TEXT};
        }}
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
