"""
PixelButton Component Module
Provides a customized button with pixel art styling.

This button component includes:
- Custom pixel art borders
- Hover and press effects
- Consistent styling with the application theme
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QSize
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class PixelButton(QPushButton):
    """
    A custom button widget with pixel art styling.
    
    Features:
    - Pixel art borders and styling
    - Hover and press states
    - Consistent theme integration
    - Custom sizing options
    """
    
    def __init__(self, text, parent=None, min_width=180, min_height=50):
        """
        Initialize a new PixelButton.
        
        Args:
            text (str): Button text
            parent (QWidget, optional): Parent widget
            min_width (int): Minimum button width
            min_height (int): Minimum button height
        """
        super().__init__(text, parent)
        self.setup_button(min_width, min_height)
    
    def setup_button(self, min_width, min_height):
        """
        Configure button appearance and behavior.
        
        Args:
            min_width (int): Minimum button width
            min_height (int): Minimum button height
        """
        # Set size constraints
        self.setMinimumSize(QSize(min_width, min_height))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Apply styling
        self.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.LIGHT};
                border-radius: 6px;
                padding: 15px;
                margin: 6px;
                text-align: center;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.MEDIUM};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
                margin: 4px 8px;  /* Slight size adjustment on hover */
            }}
            QPushButton:pressed {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
                border-color: {ThemeColors.ACCENT};
                padding: 16px 14px;  /* Pressed state effect */
            }}
        """)
