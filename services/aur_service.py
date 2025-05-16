"""
AUR Service Module
Provides functionality to interact with installed AUR packages.
"""

import subprocess
from typing import List, Dict, Any
from models.package import Package
from .aur_storage import AurPackageStorage

class AurService:
    """Service for interacting with AUR packages."""
    
    def __init__(self) -> None:
        self.storage = AurPackageStorage()
    
    def get_installed_aur_packages(self) -> List[Package]:
        """
        Get list of installed AUR packages using pacman.
        Returns a list of Package objects.
        """
        try:
            # Run pacman command to get AUR packages
            result = subprocess.run(
                ["pacman", "-Qqm"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Get package information for each AUR package
            packages: List[Package] = []
            for pkg_name in result.stdout.strip().split('\n'):
                if pkg_name:  # Skip empty lines
                    # Get detailed package info
                    pkg_info = subprocess.run(
                        ["pacman", "-Qi", pkg_name],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    # Parse package info
                    version = ""
                    description = ""
                    
                    for line in pkg_info.stdout.split('\n'):
                        if line.startswith("Version"):
                            version = line.split(":")[1].strip()
                        elif line.startswith("Description"):
                            description = line.split(":")[1].strip()
                    
                    # Update storage
                    self.storage.update_package(pkg_name, version, description)
                    
                    # Create Package object
                    packages.append(
                        Package(
                            pkg_name,
                            version,
                            "installed",
                            description=description
                        )
                    )
            
            return packages
            
        except subprocess.CalledProcessError:
            # If pacman command fails, try to load from storage
            stored_packages: Dict[str, Dict[str, Any]] = self.storage.get_all_packages()
            return [
                Package(
                    str(name),
                    str(info["version"]),
                    "installed",
                    description=str(info["description"])
                )
                for name, info in stored_packages.items()
            ]
        except Exception as e:
            print(f"Error getting AUR packages: {str(e)}")
            return []
