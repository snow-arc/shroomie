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
        # Set window flags and style
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout with better spacing
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Bigger penguin logo
        arch_logo = QLabel("🐧")
        arch_logo.setStyleSheet("""
            font-size: 72px;
            padding: 15px;
            margin: 10px;
        """)
        arch_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Package name with better contrast
        name_label = QLabel(f"Installing {self.package_name}")
        name_label.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.LARGE}px;
            color: {ThemeColors.HIGHLIGHT};
            padding: 15px;
            margin: 5px;
            background: {ThemeColors.DARK};
            border: 2px solid {ThemeColors.LIGHT};
            border-radius: 10px;
            qproperty-alignment: AlignCenter;
        """)
        name_label.setWordWrap(True)
        
        # Bigger progress bar
        self.progress = QProgressBar()
        self.progress.setMinimumHeight(35)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 10px;
                background: {ThemeColors.MEDIUM};
                text-align: center;
                font-size: {Fonts.MEDIUM}px;
                font-family: {Fonts.DECORATIVE};
                color: {ThemeColors.TEXT};
                padding: 2px;
            }}
            QProgressBar::chunk {{
                background: {ThemeColors.HIGHLIGHT};
                border-radius: 7px;
            }}
        """)
        self.progress.setRange(0, 0)
        
        # Done button with better visibility
        self.done_btn = QPushButton("✓ Done")
        self.done_btn.setMinimumHeight(50)
        self.done_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.LARGE}px;
                color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.HIGHLIGHT};
                border-radius: 10px;
                padding: 10px 30px;
                min-width: 200px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
            }}
        """)
        self.done_btn.clicked.connect(self.close)
        self.done_btn.hide()
        
        # Add widgets to layout
        layout.addWidget(arch_logo)
        layout.addWidget(name_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.done_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set larger fixed size for dialog
        self.setFixedSize(600, 400)
        
        # Set dialog style
        self.setStyleSheet(f"""
            QDialog {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 20px;
            }}
        """)
        
        # Center in parent
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
