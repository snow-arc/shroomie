"""
Main Window Module
The primary window of the application that manages the overall layout and navigation.

This module handles:
- Window initialization and setup
- Theme switching
- Page navigation
- Font loading
- Layout management
"""

from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, 
                           QStackedWidget, QPushButton)
from PyQt6.QtGui import QFontDatabase, QIcon
from PyQt6.QtCore import Qt

from ui.sidebar import Sidebar
from ui.pages import *
from ui.pages.splash_page import SplashPage
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts
from config.app_config import Config
from utils.logger import Logger
import os

logger = Logger.get_logger(__name__)

class MainWindow(QMainWindow):
    """
    Main application window.
    
    This class serves as the container for all other UI components and
    manages the overall application layout and state.
    
    Attributes:
        dark_mode (bool): Current theme state
        sidebar (Sidebar): Navigation sidebar
        pages (dict): Dictionary of available pages
        stacked_pages (QStackedWidget): Widget stack for page switching
    """
    
    def __init__(self):
        """Initialize the main window and setup UI components"""
        super().__init__()
        
        # Initialize variables
        self.dark_mode = True
        self.theme_btn = None
        self.sidebar = None
        self.pages = {}
        self.stacked_pages = None
        
        # Ensure dark theme is set immediately
        ThemeColors.set_theme(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ThemeColors.BACKGROUND};
                color: {ThemeColors.TEXT};
            }}
            QMainWindow {{
                background-color: {ThemeColors.BACKGROUND};
            }}
            * {{
                background-color: {ThemeColors.BACKGROUND};
            }}
        """)
        
        # Initialize UI
        self.init_window()
        self.load_fonts()
        self.init_ui()
        self.update_theme()  # Apply theme to all components
        logger.info("Main window initialized")
    
    def init_window(self):
        """Configure basic window properties"""
        self.setWindowTitle(Config.APP_NAME)
        self.resize(Config.WINDOW_DEFAULT_WIDTH, Config.WINDOW_DEFAULT_HEIGHT)
        self.setMinimumSize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        # Set window icon if available
        icon_path = Config.get_icon_path('logo.png')
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def init_ui(self):
        """Initialize and setup all UI components"""
        # Create theme button first
        self.setup_theme_button()
        
        # Create splash page
        self.splash_page = SplashPage()
        self.splash_page.start_clicked.connect(self.show_main_interface)
        
        # Create main interface
        self.main_widget = QWidget()
        self.layout = QHBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Initialize components
        self.setup_sidebar()
        self.setup_pages()
        
        # Set initial view to splash page
        self.setCentralWidget(self.splash_page)
        logger.debug("UI components initialized")
    
    def setup_sidebar(self):
        """Initialize and configure the sidebar"""
        self.sidebar = Sidebar()
        self.layout.addWidget(self.sidebar)
    
    def setup_pages(self):
        """Initialize and configure all application pages"""
        self.stacked_pages = QStackedWidget()
        
        # Create pages dictionary
        self.pages = {
            "aur": AurPage(),
            "delete": DeletePage(),
            "search": SearchPage(),
            "about": DevInfoPage()
        }
        
        # Add pages to stack
        for page in self.pages.values():
            self.stacked_pages.addWidget(page)
        
        # Create content container
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add theme button and pages to content
        if self.theme_btn:  # Check if theme_btn exists
            content_layout.addWidget(self.theme_btn)
        content_layout.addWidget(self.stacked_pages)
        
        self.layout.addWidget(content_container)
    
    def setup_theme_button(self):
        """Create and configure the theme toggle button"""
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.update_theme_button()
    
    def show_main_interface(self):
        """Switch from splash screen to main interface"""
        self.setCentralWidget(self.main_widget)
        self.connect_signals()
        self.change_page(0)  # Show AUR page by default
        logger.info("Showing main interface")
    
    def connect_signals(self):
        """Connect sidebar button signals to page changes"""
        self.sidebar.buttons["aur"].clicked.connect(lambda: self.change_page(0))
        self.sidebar.buttons["delete"].clicked.connect(lambda: self.change_page(1))
        self.sidebar.buttons["search"].clicked.connect(lambda: self.change_page(2))
        self.sidebar.buttons["about"].clicked.connect(lambda: self.change_page(3))
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        ThemeColors.set_theme(self.dark_mode)
        self.update_theme()
        self.update_theme_button()
        logger.debug(f"Theme changed to {'dark' if self.dark_mode else 'light'}")
    
    def update_theme_button(self):
        """Update theme button appearance based on current theme"""
        self.theme_btn.setText("🌙" if self.dark_mode else "☀️")
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                {Fonts.get_style(size=Fonts.XLARGE)}
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 20px;
                padding: 8px;
                min-width: 40px;
                max-width: 40px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
            }}
        """)
    
    def update_theme(self):
        """Update theme for all components"""
        # Update window background
        self.setStyleSheet(f"background-color: {ThemeColors.BACKGROUND};")
        
        # Update all pages
        for page in self.pages.values():
            page.setStyleSheet(f"""
                QWidget {{
                    background-color: {ThemeColors.BACKGROUND};
                    color: {ThemeColors.TEXT};
                }}
            """)
        
        # Update splash page if visible
        if self.centralWidget() == self.splash_page:
            self.splash_page.setStyleSheet(f"background-color: {ThemeColors.BACKGROUND};")
    
    def load_fonts(self):
        """Load custom fonts from resources directory"""
        try:
            fonts_dir = Config.FONTS_DIR
            font_files = {
                'PixelifySans.ttf': 'Pixelify Sans',
                'DotGothic16.ttf': 'DotGothic16',
                'PressStart2P.ttf': 'Press Start 2P'
            }
            
            for font_file, _ in font_files.items():
                font_path = fonts_dir / font_file
                if font_path.exists():
                    QFontDatabase.addApplicationFont(str(font_path))
                else:
                    logger.warning(f"Font file not found: {font_file}")
            
            logger.info("Fonts loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading fonts: {e}")
            return False
    
    def change_page(self, index):
        """
        Switch to a different page in the application.
        
        Args:
            index (int): Index of the page to display
        """
        self.stacked_pages.setCurrentIndex(index)
        logger.debug(f"Changed to page index: {index}")
        logger.debug(f"Changed to page index: {index}") 