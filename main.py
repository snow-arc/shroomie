import os
import sys

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.abspath(__file__))
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
