from typing import Dict
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QHBoxLayout)
from PyQt6.QtCore import Qt
from utils.styles import colors, PIXEL_FONTS
from components.buttons.nav_button import NavButton


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.expanded: bool = False  # Start collapsed
        self.setFixedWidth(60)  # Start with collapsed width
        self.buttons: Dict[str, NavButton] = {}
        self.button_texts: Dict[str, str] = {}
        self.logo_labels: list[QLabel] = []
        
        # Enhanced styling for better visual appeal
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors['dark']};
                border-radius: 10px;
            }}
            QWidget[class="sidebar-button"] {{
                background: {colors['medium']};
                border: 2px solid {colors['light']};
                border-radius: 8px;
                padding: 8px;
            }}
            QWidget[class="sidebar-button"]:hover {{
                background: {colors['highlight']};
                border-color: {colors['accent']};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)

        # Enhanced toggle button styling
        self.toggle_btn = QPushButton("▶")  # Changed to right arrow since we start collapsed
        self.toggle_btn.setFixedSize(35, 35)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {PIXEL_FONTS['decorative']};
                font-size: 18px;
                color: {colors['highlight']};
                background: {colors['dark']};
                border: 2px solid {colors['light']};
                border-radius: 8px;
                border-bottom: 4px solid {colors['light']};
                border-right: 4px solid {colors['light']};
                padding: 2px 0 0 0;
                margin: 2px;
            }}
            QPushButton:hover {{
                background: {colors['medium']};
                border-color: {colors['highlight']};
                color: {colors['accent']};
                margin-top: 4px;
                margin-left: 4px;
            }}
            QPushButton:pressed {{
                border-bottom: 2px solid {colors['highlight']};
                border-right: 2px solid {colors['highlight']};
                margin-top: 6px;
                margin-left: 6px;
            }}
        """)
        
        toggle_container = QWidget()
        toggle_layout = QHBoxLayout(toggle_container)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(toggle_container)
        
        # Logo section with enhanced pixel art styling
        self.logo_container = QWidget()
        self.logo_container.setFixedSize(180, 180)
        self.logo_container.hide()  # Hide logo container initially
        self.logo_container.setStyleSheet(f"""
            QWidget {{
                background: {colors['dark']};
                border: 3px solid {colors['light']};
                border-bottom: 5px solid {colors['light']};
                border-right: 5px solid {colors['light']};
                padding: 12px;
                margin: 5px;
            }}
            QWidget:hover {{
                border-color: {colors['highlight']};
                background: {colors['medium']};
                transform: translateY(-2px);
            }}
        """)
        
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setContentsMargins(5, 5, 5, 5)
        logo_layout.setSpacing(0)
        
        # Enhanced pixel art mushroom
        mushroom_art = [
            "    ▄████▄    ",
            "  ██      ██  ",
            " █  ◈   ◈   █ ",
            "█  ◇ ◆ ◇ ◆  █",
            "█  ◆ ◇ ◆ ◇  █",
            " █  ◈   ◈   █ ",
            "  ██      ██  ",
            "    ▀██▀     ",
            "     ██      ",
            "  ▀▀▀██▀▀▀   "
        ]
        
        for line in mushroom_art:
            row = QLabel(line)
            row.setStyleSheet(f"""
                font-family: monospace;
                font-size: 16px;
                color: {colors['highlight']};
                padding: 0;
                margin: 0;
                line-height: 1.2;
                text-shadow: 1px 1px {colors['accent']};
            """)
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_layout.addWidget(row)
            self.logo_labels.append(row)
        
        # Title below ASCII art
        # Enhanced app title with pixel art effect
        self.app_title = QLabel("SHROOMIE")
        self.app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_title.setStyleSheet(f"""
            font-family: {PIXEL_FONTS['decorative']};
            font-size: 20px;
            color: {colors['highlight']};
            text-shadow: 2px 2px {colors['accent']};
            background: {colors['dark']};
            border: 2px solid {colors['light']};
            border-bottom: 4px solid {colors['light']};
            border-right: 4px solid {colors['light']};
            padding: 8px 15px;
            margin-top: 15px;
        """)
        logo_layout.addWidget(self.app_title)
        
        # Main navigation buttons with pixel art styling
        nav_buttons_data = [
            ("🌿", "AUR", "aur"),
            ("🍄", "SEARCH", "search"),
            ("🌱", "DELETE", "delete")
        ]
        
        layout.addWidget(self.logo_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        
        # Enhanced button container
        self.buttons_container = QWidget()
        self.buttons_container.setStyleSheet(f"""
            QWidget {{
                background: transparent;
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        
        buttons_layout = QVBoxLayout(self.buttons_container)
        buttons_layout.setSpacing(12)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create enhanced navigation buttons
        for icon, text, key in nav_buttons_data:
            btn = self._create_nav_button(text, icon, key)
            buttons_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            # Set initial collapsed state for buttons
            if hasattr(btn, 'text_label'):
                btn.text_label.hide()
            btn.setFixedWidth(44)
            if hasattr(btn, 'button_layout'):
                btn.button_layout.setContentsMargins(5, 5, 5, 5)
        
        layout.addWidget(self.buttons_container)
        layout.addStretch()
        
        # About button with enhanced styling
        about_btn = self._create_nav_button("ABOUT", "🌲", "about")
        layout.addWidget(about_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        
        self.setLayout(layout)
        
        # Connect toggle button after everything is set up
        self.toggle_btn.clicked.connect(self.toggle_sidebar)

    def _create_nav_button(self, text: str, icon: str, key: str) -> NavButton:
        """Helper method to create consistently styled nav buttons"""
        btn = NavButton(text=text, icon=icon)
        btn.setProperty("sidebar-button", True)
        btn.setStyleSheet(f"""
            NavButton {{
                background: {colors['dark']};
                border: 2px solid {colors['light']};
                border-radius: 8px;
                padding: 8px 12px;
                margin: 4px;
            }}
            NavButton:hover {{
                background: {colors['medium']};
                border-color: {colors['highlight']};
                margin-top: 6px;
                margin-left: 6px;
            }}
            NavButton QLabel {{
                color: {colors['text']};
                font-family: {PIXEL_FONTS['decorative']};
                font-size: 16px;
            }}
            NavButton:hover QLabel {{
                color: {colors['highlight']};
            }}
            NavButton:pressed {{
                background: {colors['highlight']};
                border-color: {colors['accent']};
                margin-top: 8px;
                margin-left: 8px;
            }}
        """)
        self.buttons[key] = btn
        self.button_texts[key] = text
        return btn

    def toggle_sidebar(self) -> None:
        """Toggle sidebar expansion state with animation"""
        if self.expanded:
            # Collapse sidebar
            new_width = 60
            self.logo_container.hide()
            self.toggle_btn.setText("▶")
            
            # Update all buttons to show only icons
            for btn in self.buttons.values():
                if hasattr(btn, 'text_label'):
                    btn.text_label.hide()
                btn.setFixedWidth(44)
                if hasattr(btn, 'button_layout'):
                    btn.button_layout.setContentsMargins(5, 5, 5, 5)
        else:
            # Expand sidebar
            new_width = 220
            self.logo_container.show()
            self.toggle_btn.setText("◀")
            
            # Restore full button layouts
            for btn in self.buttons.values():
                if hasattr(btn, 'text_label'):
                    btn.text_label.show()
                btn.setFixedWidth(180)
                if hasattr(btn, 'button_layout'):
                    btn.button_layout.setContentsMargins(15, 5, 15, 5)
        
        # Animate width change
        self.setFixedWidth(new_width)
        self.expanded = not self.expanded