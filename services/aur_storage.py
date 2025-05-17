"""
AUR packages storage manager.
Handles saving and loading AUR package data to/from JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import os
import subprocess
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class AurPackageStorage(QObject):
    """Manages storage of AUR package information in JSON format."""
    
    packagesChanged = pyqtSignal()  # Signal to notify when packages change
    
    def __init__(self) -> None:
        super().__init__()
        self.storage_dir = Path.home() / ".config" / "shroomie"
        self.storage_file = self.storage_dir / "aur_packages.json"
        self._ensure_storage_exists()
        # Initial sync with system when app starts
        self.sync_with_system()

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
    
    def sync_with_system(self) -> None:
        """Sync JSON storage with actual system AUR packages"""
        try:
            # Get list of foreign packages (AUR) from pacman
            result = subprocess.run(['pacman', '-Qm'], capture_output=True, text=True)
            if result.returncode == 0:
                current_packages: Dict[str, Dict[str, Any]] = {}
                for line in result.stdout.splitlines():
                    if line.strip():
                        name, version = line.split()
                        # Get package details
                        desc = self._get_package_description(name)
                        current_packages[name] = {
                            "version": version,
                            "description": desc,
                            "repo": "AUR",
                            "install_date": self._get_install_date(name),
                            "last_updated": datetime.now().isoformat()
                        }
                
                # Compare with stored packages
                stored_packages = self._load_packages()
                if current_packages != stored_packages:
                    self._save_packages(current_packages)
                    self.packagesChanged.emit()
        except Exception as e:
            print(f"Error syncing with system: {e}")

    def _get_package_description(self, package_name: str) -> str:
        """Get package description from pacman"""
        try:
            result = subprocess.run(
                ['yay', '-Qi', package_name], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Description"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return ""

    def _get_install_date(self, package_name: str) -> str:
        """Get package installation date from pacman"""
        try:
            result = subprocess.run(
                ['yay', '-Qi', package_name], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Install Date"):
                        date_str = line.split(":", 1)[1].strip()
                        # Convert the date string to ISO format
                        try:
                            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                            return dt.isoformat()
                        except ValueError:
                            return datetime.now().isoformat()
        except Exception:
            pass
        return datetime.now().isoformat()
