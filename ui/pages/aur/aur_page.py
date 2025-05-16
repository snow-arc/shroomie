"""
AUR Page Module
Provides real-time AUR package search functionality.
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from services.aur_storage import AurPackageStorage
from services.page_communicator import PageCommunicator
from .search_section import SearchSection
from .results_grid import ResultsGrid
from .package_provider import PackageProvider
from models.package import Package

class AurPage(QWidget):
    """AUR package search and installation page."""
    
    def __init__(self) -> None:
        super().__init__()
        self.aur_storage = AurPackageStorage()
        self.communicator = PageCommunicator.instance()
        
        # Connect signals for updates
        self.communicator.packageInstalled.connect(self.refresh_packages)
        self.communicator.packageDeleted.connect(self.refresh_packages)
        self.communicator.refreshNeeded.connect(self.refresh_packages)
        
        self.package_provider = PackageProvider()
        self.refresh_packages()  # Load initial packages
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
    
    def refresh_packages(self) -> None:
        """Refresh package list from storage"""
        stored_packages = self.aur_storage.get_all_packages()
        self.all_packages = [
            Package(
                name=name,
                version=data["version"],
                repo=data.get("repo", "AUR"),  # Add repo parameter
                description=data.get("description", "")
            )
            for name, data in stored_packages.items()
        ]
        self.displayed_packages = self.all_packages.copy()
        
        # Update display if UI is initialized
        if hasattr(self, 'results_grid'):
            self.results_grid.update_display(self.displayed_packages)

    def _on_search(self, search_text: str) -> None:
        """Handle search requests."""
        if not search_text:
            self.displayed_packages = self.all_packages.copy()
        else:
            self.displayed_packages = [
                pkg for pkg in self.all_packages
                if search_text.lower() in pkg.name.lower() or
                   search_text.lower() in pkg.description.lower()
            ]
        self.results_grid.update_display(self.displayed_packages)
