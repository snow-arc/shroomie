from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class PasswordDialog(QDialog):
    passwordEntered = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Authentication Required")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon and message
        msg = QLabel("🔒 Enter your password to perform administrative tasks")
        msg.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.HIGHLIGHT};
        """)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                padding: 8px;
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 6px;
                background: {ThemeColors.MEDIUM};
            }}
        """)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        
        for btn in [self.ok_btn, cancel_btn]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-family: {Fonts.DECORATIVE};
                    font-size: {Fonts.MEDIUM}px;
                    padding: 8px 20px;
                    border: 2px solid {ThemeColors.LIGHT};
                    border-radius: 6px;
                    background: {ThemeColors.MEDIUM};
                }}
                QPushButton:hover {{
                    background: {ThemeColors.HIGHLIGHT};
                    color: {ThemeColors.DARK};
                }}
            """)
            btn_layout.addWidget(btn)
            
        self.password_input.returnPressed.connect(self.validate_and_accept)
        self.ok_btn.clicked.connect(self.validate_and_accept)
        cancel_btn.clicked.connect(self.reject)
        
        layout.addWidget(msg)
        layout.addWidget(self.password_input)
        layout.addLayout(btn_layout)
        
    def validate_and_accept(self):
        password = self.password_input.text()
        if password:
            self.passwordEntered.emit(password)
            self.accept()
    
    def get_password(self):
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            return self.password_input.text()
        return None
