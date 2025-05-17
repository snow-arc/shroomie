from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from models.package import Package
from utils.styles import *
from utils.system_checks import check_yay_installation
from typing import List

class DownloadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.packages: List[Package] = [Package(f"Downloadable {i}", "1.0.0", "main") for i in range(8)]
        self.check_dependencies()
        self.initUI()
        
    def check_dependencies(self):
        """Check if required dependencies (yay) are installed"""
        is_yay_installed, install_message = check_yay_installation()
        if not is_yay_installed:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Missing Dependencies")
            msg.setText("yay is not installed")
            msg.setInformativeText("Some features will be limited without yay.")
            msg.setDetailedText(install_message)
            msg.exec()
    
    def initUI(self):
        main_layout = QVBoxLayout()
        title = QLabel("Available Packages")
        title.setStyleSheet(page_title_style)
        
        scroll = QScrollArea()
        content = QWidget()
        grid = QGridLayout(content)
        grid.setSpacing(20)
        grid.setContentsMargins(30, 20, 30, 20)
        
        for i, pkg in enumerate(self.packages):
            row = i // 2
            col = i % 2
            grid.addWidget(self.create_download_card(pkg), row, col)
        
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def create_download_card(self, pkg: Package) -> QWidget:
        card = QWidget()
        card.setFixedSize(400, 120)
        card.setStyleSheet(download_card_style)
        
        layout = QHBoxLayout()
        
        # Left side info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(5, 5, 15, 5)  # Add right margin
        
        name_label = QLabel(pkg.name)
        name_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        name_label.setMaximumWidth(250)  # Limit package name width
        
        version_label = QLabel(f"v{pkg.version}")
        version_label.setStyleSheet("font-size: 12px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(version_label)
        info_layout.addStretch()
        
        # Right side install button
        install_btn = QPushButton("⬇️ Install")
        install_btn.setFixedSize(100, 28)  # Comfortable height with smaller width
        
        # Check if yay is available
        is_yay_installed, _ = check_yay_installation()
        if not is_yay_installed and pkg.repo.lower() == "aur":
            install_btn.setEnabled(False)
            install_btn.setToolTip("yay is required to install AUR packages")
        
        install_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {FONT_FAMILY};
                font-size: 9px;
                color: {colors['text']};
                background: {colors['medium']};
                border: 2px solid {colors['light']};
                border-radius: 4px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background: {colors['light']};
                border-color: {colors['highlight']};
                color: {colors['highlight']};
            }}
            QPushButton:disabled {{
                background: {colors['dark']};
                border-color: {colors['medium']};
                color: {colors['medium']};
            }}
        """)
        
        layout.addLayout(info_layout, stretch=1)
        layout.addWidget(install_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        card.setLayout(layout)
        return card