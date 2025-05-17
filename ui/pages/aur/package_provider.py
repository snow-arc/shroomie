"""
Package provider for AUR packages.
"""

from typing import List
from models.package import Package
from services.aur_service import AurService

class PackageProvider:
    """Provides and manages AUR packages."""
    
    def __init__(self) -> None:
        """Initialize an empty package list."""
        self.packages: List[Package] = []
        self.aur_service = AurService()
    
    def update_packages(self, packages: List[Package]) -> None:
        """Update the list of packages."""
        self.packages = packages
    
    def get_all_packages(self) -> List[Package]:
        """Get all packages."""
        return self.packages
    
    def get_sample_packages(self) -> List[Package]:
        """Get real installed AUR packages from the system."""
        return self.aur_service.get_installed_aur_packages()
    
    def filter_packages(self, search_text: str) -> List[Package]:
        """Filter packages based on search text."""
        if not search_text:
            return self.packages
        
        search_text = search_text.lower()
        return [
            pkg for pkg in self.packages
            if search_text in pkg.name.lower() or
               search_text in pkg.description.lower()
        ]
