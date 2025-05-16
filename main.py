from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys
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
