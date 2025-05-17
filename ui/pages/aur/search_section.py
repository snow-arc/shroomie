"""
Search section component for the AUR page.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class SearchSection(QWidget):
    """Search section with header and search controls."""
    
    searchRequested = pyqtSignal(str)
    refreshRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """Initialize the search section UI."""
        self.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🌿 Installed AUR Packages")
        title.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.XLARGE}px;
            color: {ThemeColors.HIGHLIGHT};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Search controls
        controls = self._create_search_controls()
        
        layout.addWidget(title)
        layout.addWidget(controls)
    
    def _create_search_controls(self):
        """Create search input and buttons."""
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(15)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search in installed AUR packages...")
        self.search_input.setMinimumHeight(45)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QLineEdit:focus {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
        self.search_input.returnPressed.connect(self._emit_search)
        
        # Search button
        search_btn = QPushButton("🔎 Search")
        search_btn.setMinimumHeight(45)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
            }}
        """)
        search_btn.clicked.connect(self._emit_search)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
            }}
        """)
        refresh_btn.clicked.connect(self.refreshRequested.emit)
        
        controls_layout.addWidget(self.search_input, stretch=1)
        controls_layout.addWidget(search_btn)
        controls_layout.addWidget(refresh_btn)
        
        return controls
    
    def _emit_search(self):
        """Emit search signal with current input text."""
        self.searchRequested.emit(self.search_input.text())
