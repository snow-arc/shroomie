"""
PackageCard Component Module
Provides a reusable card component for displaying package information.

Features:
- Well-organized package information display
- Install button with hover effects
- Flexible sizing and spacing
- Consistent theme integration
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts
import random

class PackageCard(QWidget):
    """
    A card component for displaying package information.
    
    Attributes:
        package: The package to display information for
        show_install_button: Whether to show the install button
        show_version: Whether to show version information
    """
    
    def __init__(self, package, show_install_button=True, show_version=True, parent=None):
        super().__init__(parent)
        self.package = package
        self.show_install_button = show_install_button
        self.show_version = show_version
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.update_random_colors)
        self.color_timer.setInterval(100)  # Update every 100ms
        self.is_animating = False
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the card's user interface layout and styling"""
        # Set fixed height to prevent overlapping
        self.setFixedHeight(180)
        
        # Main card layout with proper spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Info container at the top
        info_container = self.create_info_container()
        main_layout.addWidget(info_container)
        
        # Add stretch to push button to bottom
        main_layout.addStretch()
        
        # Button container at the bottom if enabled
        if self.show_install_button:
            button_container = self.create_button_container()
            main_layout.addWidget(button_container)
        
        # Apply card styling with hover effects
        self.setStyleSheet(f"""
            PackageCard {{
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 10px;
                margin: 5px;
            }}
            PackageCard:hover {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
    
    def create_info_container(self):
        """Create and style the package information container"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)
        
        # Package name with icon
        name_label = QLabel(f"📦 {self.package.name}")
        name_label.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.LARGE}px;
            color: {ThemeColors.HIGHLIGHT};
            letter-spacing: 1px;
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        # Version info if enabled
        if self.show_version:
            version_label = QLabel(f"Version {self.package.version}")
            version_label.setStyleSheet(f"""
                font-family: {Fonts.SECONDARY};
                color: {ThemeColors.TEXT};
                font-size: {Fonts.MEDIUM}px;
            """)
            version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(version_label)
        
        return container
    
    def create_button_container(self):
        """Create and style the button container"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Install button with improved styling
        install_btn = QPushButton("📥 Install")
        install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        install_btn.setFixedHeight(36)
        install_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.HIGHLIGHT};
                border-radius: 6px;
                padding: 4px 20px;
                letter-spacing: 1px;
                min-width: 120px;
                transition: all 0.3s;
            }}
            QPushButton:hover {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
                transform: scale(1.1);
                border-color: {ThemeColors.ACCENT};
                box-shadow: 0 0 10px {ThemeColors.ACCENT};
            }}
            QPushButton:pressed {{
                padding: 6px 18px;
                transform: scale(0.95);
                background: {ThemeColors.ACCENT};
            }}
        """)
        
        layout.addWidget(install_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return container
    
    def mousePressEvent(self, event):
        """Handle mouse click to toggle color animation"""
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_animating:
                self.start_color_animation()
            else:
                self.stop_color_animation()
    
    def start_color_animation(self):
        """Start the color animation"""
        self.is_animating = True
        self.color_timer.start()
    
    def stop_color_animation(self):
        """Stop the color animation and reset colors"""
        self.is_animating = False
        self.color_timer.stop()
        self.reset_colors()
    
    def reset_colors(self):
        """Reset to default colors"""
        self.setStyleSheet(f"""
            PackageCard {{
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 10px;
                margin: 5px;
            }}
            PackageCard:hover {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
    
    def generate_random_color(self):
        """Generate a random pastel color"""
        hue = random.random()
        saturation = random.uniform(0.5, 0.7)
        value = random.uniform(0.8, 1.0)
        
        # Convert HSV to RGB
        c = QColor()
        c.setHsvF(hue, saturation, value)
        return c.name()
    
    def update_random_colors(self):
        """Update card with new random colors"""
        bg_color = self.generate_random_color()
        border_color = self.generate_random_color()
        
        self.setStyleSheet(f"""
            PackageCard {{
                background: {bg_color};
                border: 4px solid {border_color};
                border-radius: 10px;
                margin: 5px;
                transition: all 0.3s;
            }}
        """)
