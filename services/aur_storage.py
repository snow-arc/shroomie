"""
AUR packages storage manager.
Handles saving and loading AUR package data to/from JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import os

class AurPackageStorage:
    """Manages storage of AUR package information in JSON format."""
    
    def __init__(self) -> None:
        self.storage_dir = Path.home() / ".config" / "shroomie"
        self.storage_file = self.storage_dir / "aur_packages.json"
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and file exist."""
        os.makedirs(self.storage_dir, exist_ok=True)
        if not self.storage_file.exists():
            self._save_packages({})
    
    def _save_packages(self, packages: Dict[str, Dict[str, Any]]) -> None:
        """Save packages data to JSON file."""
        with open(self.storage_file, 'w') as f:
            json.dump(packages, f, indent=2)
    
    def _load_packages(self) -> Dict[str, Dict[str, Any]]:
        """Load packages data from JSON file."""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def update_package(self, name: str, version: str, description: str, repo: str = "AUR") -> None:
        """Update or add a package in storage."""
        packages = self._load_packages()
        packages[name] = {
            "version": version,
            "description": description,
            "repo": repo,
            "install_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        self._save_packages(packages)
    
    def remove_package(self, name: str) -> None:
        """Remove a package from storage."""
        packages = self._load_packages()
        if name in packages:
            del packages[name]
            self._save_packages(packages)
    
    def get_all_packages(self) -> Dict[str, Dict[str, Any]]:
        """Get all stored packages."""
        return self._load_packages()
    
    def get_package(self, name: str) -> Dict[str, Any]:
        """Get information for a specific package."""
        packages = self._load_packages()
        return packages.get(name, {})
