"""
AUR Page Module
Provides real-time AUR package search functionality.

Features:
- Instant search as you type
- Grid layout package display
- Package installation buttons 
- Responsive design with hover effects
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QScrollArea, QGridLayout, QLabel)
from PyQt6.QtCore import Qt
from models.package import Package
from components.cards.package_card import PackageCard
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class AurPage(QWidget):
    """AUR package search and installation page."""
    
    def __init__(self):
        super().__init__()
        # Initialize with sample installed AUR packages
        self.all_packages = [
            Package("yay-bin", "12.1.0", "installed",
                   description="Yet another yogurt. Installed on 2025-01-15"),
            Package("paru", "2.0.1", "installed", 
                   description="Feature packed AUR helper. Installed on 2025-02-20"),
            Package("pamac-all", "10.4.3", "installed",
                   description="Package manager with AUR support. Installed on 2025-03-10"),
            Package("visual-studio-code-bin", "1.85.1", "installed",
                   description="VS Code from the AUR. Installed on 2025-04-01"),
            Package("spotify", "1.2.22", "installed",
                   description="Music streaming client. Installed on 2025-04-15"),
            Package("chrome-gnome-shell", "10.1", "installed",
                   description="A secure package manager for Arch Linux and the AUR"),
            Package("pacaur", "4.8.7", "aur",
                   description="An AUR helper that minimizes user interaction"),
            Package("trizen", "1.65", "aur",
                   description="Lightweight AUR package manager"),
            Package("octopi", "0.15.0", "aur",
                   description="A powerful Qt-based package manager for Arch Linux"),
            Package("pamac-all", "10.4.3", "aur",
                   description="A fully featured Gtk package manager with AUR, flatpak and snap support")
        ]
        self.displayed_packages = self.all_packages.copy()
        self.initUI()
    
    def initUI(self):
        """Setup the user interface components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create search section
        search_section = self.create_header()
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
    
    def create_header(self):
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
        title = QLabel("🌿 Installed AUR Packages")
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
        self.search_input.setPlaceholderText("Search in installed AUR packages...")
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
        self.search_input.textChanged.connect(self.filter_packages)
        
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
        search_btn.clicked.connect(self.filter_packages)
        
        controls_layout.addWidget(self.search_input, stretch=1)
        controls_layout.addWidget(search_btn)
        
        layout.addWidget(title)
        layout.addWidget(controls)
        
        return container
    
    def filter_packages(self):
        """Filter packages based on search text"""
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
            f"Installed AUR packages: {result_count}"
        )
        
        # Clear current grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.displayed_packages:
            # Show no results message
            no_results = QLabel("No installed AUR packages found 🔍")
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
            return            # Add package cards to grid without install button
        for i, pkg in enumerate(self.displayed_packages):
            row = i // 2  # 2 columns
            col = i % 2
            card = PackageCard(pkg, show_install_button=False)  # Removed install button
            self.grid.addWidget(card, row, col)