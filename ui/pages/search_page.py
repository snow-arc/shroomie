"""
Search Page Module
Provides real-time package search functionality.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QScrollArea, QGridLayout, QLabel)
from PyQt6.QtCore import Qt
from models.package import Package
from components.cards.package_card import PackageCard
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize with sample packages (replace with real data later)
        self.all_packages = [
            Package(f"Package {i}", f"1.{i}.0", "main", 
                   description=f"Sample package {i} for testing") 
            for i in range(20)
        ]
        self.displayed_packages = self.all_packages.copy()
        self.initUI()
    
    def initUI(self):
        """Setup the user interface components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create search section
        search_section = self.create_search_section()
        main_layout.addWidget(search_section)
        
        # Create results section
        self.results_container = QWidget()
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(10)
        
        # Results counter
        self.results_counter = QLabel()
        self.results_counter.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            padding: 10px;
        """)
        results_layout.addWidget(self.results_counter)
        
        # Scrollable results grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 14px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: rgba(124, 255, 186, 0.3);
                border-radius: 7px;
                min-height: 30px;
            }
        """)
        
        self.content = QWidget()
        self.grid = QGridLayout(self.content)
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(10, 10, 10, 10)
        
        scroll.setWidget(self.content)
        results_layout.addWidget(scroll)
        
        main_layout.addWidget(self.results_container)
        self.display_packages()
    
    def create_search_section(self):
        """Create enhanced search controls"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔍 Package Search")
        title.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.XLARGE}px;
            color: {ThemeColors.HIGHLIGHT};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Search controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(15)
        
        # Search input with real-time search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter package name to search...")
        self.search_input.setMinimumHeight(45)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QLineEdit:focus {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        
        # Search button
        search_btn = QPushButton("🔎 Search")
        search_btn.setMinimumHeight(45)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
            }}
        """)
        search_btn.clicked.connect(self.perform_search)
        
        controls_layout.addWidget(self.search_input, stretch=1)
        controls_layout.addWidget(search_btn)
        
        layout.addWidget(title)
        layout.addWidget(controls)
        
        return container
    
    def on_search_text_changed(self, text):
        """Handle real-time search as user types"""
        self.perform_search()
    
    def perform_search(self):
        """Perform the actual search operation"""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            self.displayed_packages = self.all_packages
        else:
            self.displayed_packages = [
                pkg for pkg in self.all_packages
                if search_text in pkg.name.lower() or
                   search_text in pkg.description.lower()
            ]
        
        self.display_packages()
    
    def display_packages(self):
        """Display current filtered packages"""
        # Update results counter
        result_count = len(self.displayed_packages)
        self.results_counter.setText(
            f"Found {result_count} package{'s' if result_count != 1 else ''}"
        )
        
        # Clear current grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.displayed_packages:
            # Show no results message
            no_results = QLabel("No packages found 😔")
            no_results.setStyleSheet(f"""
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.LARGE}px;
                color: {ThemeColors.ACCENT};
                padding: 30px;
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 10px;
            """)
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid.addWidget(no_results, 0, 0, 1, 2)
            return
        
        # Add package cards to grid
        for i, pkg in enumerate(self.displayed_packages):
            row = i // 2  # 2 columns
            col = i % 2
            card = PackageCard(pkg, show_install_button=True)
            self.grid.addWidget(card, row, col)