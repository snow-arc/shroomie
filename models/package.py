"""
Package Model Module
Defines the Package class representing a software package.

This module contains the core Package class that represents
software packages in the system, whether from AUR or installed locally.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Package:
    """
    Represents a software package.
    
    This class holds all relevant information about a package,
    including its metadata and current status.
    
    Attributes:
        name (str): Package name
        version (str): Package version
        repo (str): Repository name (e.g., 'community', 'aur')
        description (str): Package description
        status (str): Current status (e.g., 'Not Installed', 'Installed')
        install_date (Optional[datetime]): Installation date if installed
        dependencies (List[str]): List of package dependencies
        maintainer (Optional[str]): Package maintainer
        license (Optional[str]): Package license
    """
    
    name: str
    version: str
    repo: str
    description: str = "No description available"
    status: str = "Not Installed"
    install_date: Optional[datetime] = None
    dependencies: List[str] = None
    maintainer: Optional[str] = None
    license: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values after dataclass initialization"""
        if self.dependencies is None:
            self.dependencies = []
    
    def __str__(self) -> str:
        """Return string representation of the package"""
        return f"{self.name} ({self.version})"
    
    def get_status_emoji(self) -> str:
        """
        Get an emoji representing the package status.
        
        Returns:
            str: Status emoji
        """
        status_emojis = {
            "Not Installed": "📦",
            "Installed": "✅",
            "Updates Available": "🔄",
            "Installing": "⏳",
            "Removing": "🗑️",
            "Error": "❌"
        }
        return status_emojis.get(self.status, "❓")
    
    def is_installed(self) -> bool:
        """
        Check if the package is installed.
        
        Returns:
            bool: True if installed, False otherwise
        """
        return self.status == "Installed"
    
    def needs_update(self) -> bool:
        """
        Check if the package has updates available.
        
        Returns:
            bool: True if updates available, False otherwise
        """
        return self.status == "Updates Available"
    
    def set_installed(self, version: str, install_date: datetime = None):
        """
        Mark the package as installed.
        
        Args:
            version (str): Installed version
            install_date (datetime, optional): Installation date
        """
        self.version = version
        self.status = "Installed"
        self.install_date = install_date or datetime.now()
    
    def set_uninstalled(self):
        """Mark the package as not installed"""
        self.status = "Not Installed"
        self.install_date = None