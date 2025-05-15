"""
Navigation Button Component
Custom button with pixel art styling for the sidebar
"""
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from utils.themes.colors import ThemeColors as Colors

class NavButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self.setProperty("class", "nav-button")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(45)
        
        # Setup layout
        self.button_layout = QHBoxLayout(self)
        self.button_layout.setContentsMargins(15, 5, 15, 5)
        self.button_layout.setSpacing(12)
        
        # Add icon if provided
        if icon:
            self.icon_label = QLabel(icon)
            self.icon_label.setStyleSheet(f"""
                color: {Colors.HIGHLIGHT};
                font-size: 16px;
                padding: 0;
                margin: 0;
            """)
            self.button_layout.addWidget(self.icon_label)
        
        # Add text
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("""
            padding: 0;
            margin: 0;
        """)
        self.button_layout.addWidget(self.text_label)
        
    def setIcon(self, icon):
        """Update button icon"""
        if hasattr(self, 'icon_label'):
            self.icon_label.setText(icon)
        else:
            self.icon_label = QLabel(icon)
            self.icon_label.setStyleSheet(f"""
                color: {Colors.HIGHLIGHT};
                font-size: 16px;
                padding: 0;
                margin: 0;
            """)
            self.button_layout.insertWidget(0, self.icon_label)
    
    def setText(self, text):
        """Update button text"""
        self.text_label.setText(text)
