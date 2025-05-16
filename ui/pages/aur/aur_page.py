"""
AUR Page Module
Provides real-time AUR package search functionality.
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .search_section import SearchSection
from .results_grid import ResultsGrid
from .package_provider import PackageProvider
from models.package import Package

class AurPage(QWidget):
    """AUR package search and installation page."""
    
    def __init__(self) -> None:
        super().__init__()
        self.package_provider = PackageProvider()
        self.all_packages: List[Package] = self.package_provider.get_sample_packages()
        self.displayed_packages: List[Package] = self.all_packages.copy()
        self.initUI()
    
    def initUI(self) -> None:
        """Setup the user interface components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create search section
        self.search_section = SearchSection()
        self.search_section.searchRequested.connect(self._on_search)
        main_layout.addWidget(self.search_section)
        
        # Create results grid
        self.results_grid = ResultsGrid()
        main_layout.addWidget(self.results_grid)
        
        # Initial display
        self.results_grid.update_display(self.displayed_packages)
    
    def _on_search(self, search_text: str) -> None:
        """Handle search requests."""
        self.displayed_packages = self.package_provider.filter_packages(
            self.all_packages, search_text
        )
        self.results_grid.update_display(self.displayed_packages)
