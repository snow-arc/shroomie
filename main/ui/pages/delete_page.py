"""
Delete Page Module
Provides package removal functionality with search capabilities.

Features:
- Package search
- List of installed packages
- Safe package removal
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, 
                            QPushButton, QHBoxLayout, QLineEdit)
from PyQt6.QtCore import Qt
from models.package import Package
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class DeletePage(QWidget):
    """Package deletion page with search functionality"""
    
    def __init__(self):
        super().__init__()
        self.all_packages = [Package(f"Package {i}", f"1.{i}.0", "main") for i in range(8)]
        self.displayed_packages = self.all_packages.copy()
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Add header with warning
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Add search section
        search_section = self.create_search_section()
        main_layout.addWidget(search_section)

        # Add scrollable package list
        packages_section = self.create_packages_section()
        main_layout.addWidget(packages_section)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create warning header section"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.WARNING};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Warning title
        title = QLabel("⚠️ Package Removal")
        title.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.XLARGE}px;
            color: {ThemeColors.WARNING};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Warning message
        warning = QLabel("Select packages to remove. This action cannot be undone!")
        warning.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
        """)
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(warning)
        
        return container
    
    def create_search_section(self):
        """Create search input section"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search installed packages...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QLineEdit:focus {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
        self.search_input.textChanged.connect(self.filter_packages)
        
        # Search button
        search_btn = QPushButton("🔍 Search")
        search_btn.setMinimumHeight(40)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.WARNING};
                color: {ThemeColors.WARNING};
            }}
        """)
        search_btn.clicked.connect(self.filter_packages)
        
        layout.addWidget(self.search_input, stretch=1)
        layout.addWidget(search_btn)
        
        return container
    
    def create_packages_section(self):
        """Create scrollable packages list section"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 107, 107, 0.3);
                border-radius: 6px;
                min-height: 30px;
            }
        """)

        content = QWidget()
        self.packages_layout = QVBoxLayout(content)
        self.packages_layout.setSpacing(10)
        
        # Initial display of packages
        self.display_packages()
        
        scroll.setWidget(content)
        return scroll
    
    def filter_packages(self):
        """Filter packages based on search text"""
        search_text = self.search_input.text().lower()
        self.displayed_packages = [
            pkg for pkg in self.all_packages
            if search_text in pkg.name.lower()
        ]
        self.display_packages()
    
    def display_packages(self):
        """Display filtered packages in the list"""
        # Clear current list
        while self.packages_layout.count():
            item = self.packages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.displayed_packages:
            # Show no results message
            no_results = QLabel("No packages found 🔍")
            no_results.setStyleSheet(f"""
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.LARGE}px;
                color: {ThemeColors.ACCENT};
                padding: 20px;
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
            """)
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.packages_layout.addWidget(no_results)
            return
        
        # Add package items
        for pkg in self.displayed_packages:
            self.add_package_item(pkg)
    
    def add_package_item(self, pkg):
        """Create and add a package item to the list"""
        item = QWidget()
        item.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 12px;
            }}
            QWidget:hover {{
                border-color: {ThemeColors.WARNING};
                background: {ThemeColors.DARK};
            }}
        """)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 8, 15, 8)

        # Package info with pixel border
        info = QLabel(f"📦 {pkg.name} (v{pkg.version})")
        info.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            background: {ThemeColors.DARK};
            border: 2px solid {ThemeColors.LIGHT};
            border-radius: 4px;
            padding: 8px 15px;
        """)

        # Delete button with warning colors
        delete_btn = QPushButton("🗑️ Remove")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.WARNING};
                background: transparent;
                border: 3px solid {ThemeColors.WARNING};
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.WARNING};
                color: {ThemeColors.DARK};
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_package(item, pkg.name))

        layout.addWidget(info, stretch=1)
        layout.addWidget(delete_btn)
        self.packages_layout.addWidget(item)

    def delete_package(self, item, package_name):
        """Handle package deletion"""
        # Here you would add actual package deletion logic
        item.setParent(None)  # Remove from UI
        # Update package lists
        self.all_packages = [pkg for pkg in self.all_packages if pkg.name != package_name]
        self.displayed_packages = [pkg for pkg in self.displayed_packages if pkg.name != package_name]