from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                            QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class SplashPage(QWidget):
    start_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # Set dark theme immediately during initialization
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ThemeColors.BACKGROUND};
                color: {ThemeColors.TEXT};
            }}
            QWidget#splash_container {{
                background-color: {ThemeColors.BACKGROUND};
            }}
        """)
        self.initUI()
    
    def initUI(self):
        
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 40, 20, 40)
        
        # Pixel art decorative container
        pixel_container = QWidget()
        pixel_container.setFixedSize(200, 200)
        pixel_container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 8px;
                box-shadow: 0 0 20px {ThemeColors.ACCENT};
            }}
        """)
        # Create pixel art mushroom decoration
        decor_layout = QVBoxLayout(pixel_container)
        decor_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        mushroom_art = [
            "    ⬛⬛⬛⬛    ",
            "  ⬛🟥🟥🟥🟥⬛  ",
            "⬛🟥⬜🟥🟥🟥🟥⬛",
            "⬛🟥🟥🟥🟥🟥🟥⬛",
            "  ⬛⬛🟫⬛⬛  ",
            "    ⬛🟫⬛    ",
            "    ⬛🟫⬛    ",
            "  ⬛🟫🟫🟫⬛  ",
            "⬛⬛⬛⬛⬛⬛⬛⬛"
        ]
        
        for row in mushroom_art:
            pixel_row = QLabel(row)
            pixel_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pixel_row.setStyleSheet("""
                font-family: monospace;
                font-size: 20px;
                line-height: 1;
                padding: 0;
                margin: 0;
            """)
            decor_layout.addWidget(pixel_row)
        
        # Title with pixel art style
        title = QLabel("SHROOMIE")
        title.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: 32px;
            color: {ThemeColors.HIGHLIGHT};
            padding: 15px 25px;
            background-color: {ThemeColors.DARK};
            border: 4px solid {ThemeColors.HIGHLIGHT};
            border-radius: 8px;
            box-shadow: 0 0 15px {ThemeColors.ACCENT};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start button with pixel art style
        start_btn = QPushButton("[ PRESS START! ]")
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.setFixedSize(240, 50)
        start_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.LARGE}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 6px;
                padding: 8px 16px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.ACCENT};
                color: {ThemeColors.HIGHLIGHT};
                transform: scale(1.1);
                box-shadow: 0 0 15px {ThemeColors.ACCENT};
            }}
            QPushButton:pressed {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
                border-color: {ThemeColors.ACCENT};
                transform: scale(0.95);
            }}
        """)
        start_btn.clicked.connect(self.start_clicked.emit)
        
        # Add pixel art decorative frame
        frame_top = QLabel("╔══════════╗")
        frame_bottom = QLabel("╚══════════╝")
        for frame in [frame_top, frame_bottom]:
            frame.setStyleSheet(f"""
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.ACCENT};
                margin: 5px;
                text-shadow: 0 0 5px {ThemeColors.ACCENT};
            """)
            frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(frame_top)
        layout.addWidget(pixel_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(frame_bottom)
        layout.addStretch()
        
        self.setLayout(layout)
