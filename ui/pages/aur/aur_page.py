"""
AUR Page Module
Provides real-time AUR package search functionality.
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
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
        self.package_provider = PackageProvider()
        self.communicator = PageCommunicator.instance()
        
        # Connect signals for updates
        self.communicator.packageInstalled.connect(self.refresh_packages)
        self.communicator.packageDeleted.connect(self.refresh_packages)
        self.communicator.refreshNeeded.connect(self.refresh_packages)
        
        self.initUI()
        self.refresh_packages()  # Load initial packages
    
    def initUI(self) -> None:
        """Setup the user interface components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create search section
        self.search_section = SearchSection()
        self.search_section.searchRequested.connect(self._on_search)
        self.search_section.refreshRequested.connect(self.manual_refresh)
        main_layout.addWidget(self.search_section)
        
        # Create results grid
        self.results_grid = ResultsGrid()
        main_layout.addWidget(self.results_grid)
    
    def manual_refresh(self) -> None:
        """Handle manual refresh request"""
        # First sync with system to get latest changes
        self.aur_storage.sync_with_system()
        # Then refresh the display
        self.refresh_packages()

    def refresh_packages(self) -> None:
        """Refresh package list from storage"""
        stored_packages = self.aur_storage.get_all_packages()
        self.package_provider.update_packages([
            Package(
                name=name,
                version=data["version"],
                description=data.get("description", ""),
                repo=data.get("repo", "AUR")
            )
            for name, data in stored_packages.items()
        ])
        self.results_grid.update_display(self.package_provider.get_all_packages())

    def _on_search(self, search_text: str) -> None:
        """Handle search requests"""
        packages = self.package_provider.filter_packages(search_text)
        self.results_grid.update_display(packages)
