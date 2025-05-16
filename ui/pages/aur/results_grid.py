"""
Results grid component for the AUR page.
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QLabel
from PyQt6.QtCore import Qt
# Fix imports to use absolute paths
from components.cards.package_card import PackageCard
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts
from models.package import Package

class ResultsGrid(QScrollArea):
    """Grid display for AUR package results."""
    
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
    
    def initUI(self) -> None:
        """Initialize the results grid UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Results counter
        self.results_counter = QLabel()
        self.results_counter.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            padding: 10px;
        """)
        layout.addWidget(self.results_counter)
        
        # Scrollable results area
        scroll = self._create_scroll_area()
        layout.addWidget(scroll)
    
    def _create_scroll_area(self) -> QScrollArea:
        """Create scrollable area for package cards."""
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
        return scroll
    
    def update_display(self, packages: List[Package]) -> None:
        """Update the grid with filtered packages."""
        # Update counter
        count = len(packages)
        self.results_counter.setText(f"Installed AUR packages: {count}")
        
        # Clear current grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.deleteLater()
        
        if not packages:
            self._show_no_results()
            return
        
        # Add package cards
        for i, pkg in enumerate(packages):
            row = i // 2
            col = i % 2
            card = self.create_package_card(pkg)
            self.grid.addWidget(card, row, col)
    
    def create_package_card(self, pkg):
        card = QWidget()
        card.setFixedSize(280, 100)  # تعديل الحجم ليكون أصغر
        card.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 10px;
            }}
            QWidget:hover {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # Package name
        name = QLabel(f"📦 {pkg.name}")
        name.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            background: {ThemeColors.DARK};
            border-radius: 4px;
            padding: 5px;
        """)
        name.setWordWrap(True)

        # Version
        version = QLabel(f"Version: {pkg.version}")
        version.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.SMALL}px;
            color: {ThemeColors.TEXT};
        """)

        layout.addWidget(name)
        layout.addWidget(version)
        return card
    
    def _show_no_results(self) -> None:
        """Display no results message."""
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
