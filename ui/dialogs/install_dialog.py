from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt6.QtCore import Qt, QPoint
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class InstallDialog(QDialog):
    def __init__(self, package_name, parent=None):
        super().__init__(parent)
        self.package_name = package_name
        self.setModal(True)  # Make dialog modal
        self.setup_ui()
    
    def setup_ui(self):
        # Set proper window flags for Wayland
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(f"""
            QDialog {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 15px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Arch Logo
        arch_logo = QLabel("🐧")
        arch_logo.setStyleSheet(f"font-size: 48px;")
        arch_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Package Name
        name_label = QLabel(f"Installing {self.package_name}")
        name_label.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.LARGE}px;
            color: {ThemeColors.HIGHLIGHT};
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                background: {ThemeColors.MEDIUM};
                height: 24px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: {ThemeColors.HIGHLIGHT};
                border-radius: 4px;
            }}
        """)
        self.progress.setRange(0, 0)  # Indeterminate progress
        
        layout.addWidget(arch_logo)
        layout.addWidget(name_label)
        layout.addWidget(self.progress)
        
        # Add Done Button
        self.done_btn = QPushButton("✓ Done")
        self.done_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.HIGHLIGHT};
                border-radius: 6px;
                padding: 8px 25px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
            }}
        """)
        self.done_btn.clicked.connect(self.close)
        self.done_btn.hide()
        
        layout.addWidget(self.done_btn)
        
        self.setFixedSize(400, 250)
        
        # Ensure proper positioning
        if self.parent():
            parent_center = self.parent().geometry().center()
            self.move(
                parent_center.x() - self.width() // 2,
                parent_center.y() - self.height() // 2
            )
        
    def show_success(self):
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.done_btn.show()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragPos'):
            diff = event.globalPosition().toPoint() - self.dragPos
            newPos = self.pos() + QPoint(diff.x(), diff.y())
            self.move(newPos)
            self.dragPos = event.globalPosition().toPoint()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()  # Ensure dialog gets focus
