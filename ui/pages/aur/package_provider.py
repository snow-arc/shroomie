"""
Package data provider for the AUR page.
"""

from typing import List
# Fix imports to use absolute paths
from models.package import Package
from services.aur_service import AurService

class PackageProvider:
    """Provider for AUR package data."""
    
    def __init__(self) -> None:
        self.aur_service = AurService()
    
    def get_sample_packages(self) -> List[Package]:
        """Get real installed AUR packages from the system."""
        return self.aur_service.get_installed_aur_packages()
    
    def filter_packages(self, packages: List[Package], search_text: str) -> List[Package]:
        """Filter packages based on search text."""
        search_text = search_text.lower().strip()
        
        if not search_text:
            return packages
        
        return [
            pkg for pkg in packages
            if search_text in pkg.name.lower() or
               search_text in pkg.description.lower()
        ]
