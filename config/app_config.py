"""
Application Configuration Module
Centralizes all configuration settings for the Shroomie package manager.

This module contains settings for:
- Application behavior
- UI customization
- Package management
- System paths
"""

import os
from pathlib import Path

class Config:
    """
    Application configuration settings.
    
    This class provides centralized access to all configuration settings
    used throughout the application.
    """
    
    # Application metadata
    APP_NAME = "Shroomie"
    VERSION = "1.0.0"
    DESCRIPTION = "A pixel art styled AUR package manager"
    
    # UI Configuration
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    WINDOW_DEFAULT_WIDTH = 1000
    WINDOW_DEFAULT_HEIGHT = 720
    
    # Sidebar Configuration
    SIDEBAR_EXPANDED_WIDTH = 220
    SIDEBAR_COLLAPSED_WIDTH = 60
    
    # Grid Layout
    GRID_COLUMNS = 3
    GRID_SPACING = 15
    GRID_MARGINS = (20, 15, 20, 15)
    
    # Package Display
    PACKAGES_PER_PAGE = 12
    PACKAGE_CARD_MIN_HEIGHT = 120
    
    # File System Paths
    BASE_DIR = Path(__file__).parent.parent
    RESOURCES_DIR = BASE_DIR / "resources"
    FONTS_DIR = RESOURCES_DIR / "fonts"
    ICONS_DIR = RESOURCES_DIR / "icons"
    
    # Cache Settings
    CACHE_DIR = BASE_DIR / "cache"
    CACHE_EXPIRE_DAYS = 1
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        dirs = [cls.CACHE_DIR, cls.RESOURCES_DIR, cls.FONTS_DIR, cls.ICONS_DIR]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_font_path(cls, font_name):
        """
        Get the full path to a font file.
        
        Args:
            font_name (str): Name of the font file
            
        Returns:
            Path: Full path to the font file
        """
        return cls.FONTS_DIR / font_name
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """
        Get the full path to an icon file.
        
        Args:
            icon_name (str): Name of the icon file
            
        Returns:
            Path: Full path to the icon file
        """
        return cls.ICONS_DIR / icon_name
