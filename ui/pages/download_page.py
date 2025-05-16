from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from models.package import Package
from utils.styles import *

class DownloadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.packages = [Package(f"Downloadable {i}", "1.0.0", "main") for i in range(8)]
        self.initUI()
        
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
    
    def create_download_card(self, pkg):
        card = QWidget()
        card.setFixedSize(400, 120)
        card.setStyleSheet(download_card_style)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"⬇️ {pkg.name}"))
        layout.addWidget(QLabel(f"Version: {pkg.version}"))
        return card