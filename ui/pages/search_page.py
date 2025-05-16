"""
Search Page Module
Provides real-time package search functionality.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QScrollArea, QLabel)
from PyQt6.QtCore import Qt
import subprocess
from models.package import Package
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 200
        self.current_page = 0
        self.all_packages = self.fetch_packages()
        self.displayed_packages = self.all_packages[:self.page_size]
        self.initUI()
    
    def fetch_packages(self):
        """Fetch packages using yay command"""
        try:
            result = subprocess.run(['yay', '-Ss', ''], capture_output=True, text=True)
            packages = []
            current_pkg = None
            
            for line in result.stdout.split('\n'):
                if line.startswith('    '): # Description line
                    if current_pkg:
                        current_pkg.description = line.strip()
                else:
                    parts = line.split('/')
                    if len(parts) >= 2:
                        repo_pkg = parts[1].split()
                        if len(repo_pkg) >= 2:
                            name = repo_pkg[0]
                            version = repo_pkg[1]
                            repo = parts[0]
                            current_pkg = Package(name, version, repo)
                            packages.append(current_pkg)
            
            return packages
        except Exception as e:
            print(f"Error fetching packages: {e}")
            return []

    def initUI(self):
        """Setup the user interface components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        search_section = self.create_search_section()
        main_layout.addWidget(search_section)
        
        # Create results section
        self.results_container = QWidget()
        results_layout = QVBoxLayout(self.results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(10)
        
        # Results counter
        self.results_counter = QLabel()
        self.results_counter.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            padding: 10px;
        """)
        results_layout.addWidget(self.results_counter)
        
        # Scrollable results list
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
                background: rgba(124, 255, 186, 0.3);
                border-radius: 6px;
                min-height: 30px;
            }
        """)
        
        self.content = QWidget()
        self.packages_layout = QVBoxLayout(self.content)
        self.packages_layout.setSpacing(10)
        self.packages_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(self.content)
        results_layout.addWidget(scroll)
        
        main_layout.addWidget(self.results_container)
        self.display_packages()
    
    def create_search_section(self):
        """Create enhanced search controls"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.HIGHLIGHT};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔍 Package Search")
        title.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.XLARGE}px;
            color: {ThemeColors.HIGHLIGHT};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Search controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(15)
        
        # Search input with real-time search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter package name to search...")
        self.search_input.setMinimumHeight(45)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QLineEdit:focus {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        
        # Search button
        search_btn = QPushButton("🔎 Search")
        search_btn.setMinimumHeight(45)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
            }}
        """)
        search_btn.clicked.connect(self.perform_search)
        
        controls_layout.addWidget(self.search_input, stretch=1)
        controls_layout.addWidget(search_btn)
        
        layout.addWidget(title)
        layout.addWidget(controls)
        
        return container
    
    def on_search_text_changed(self, text):
        """Handle real-time search as user types"""
        self.perform_search()
    
    def perform_search(self):
        """Perform the actual search operation"""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            self.displayed_packages = self.all_packages[:self.page_size]
        else:
            self.displayed_packages = [
                pkg for pkg in self.all_packages
                if search_text in pkg.name.lower() or
                   search_text in pkg.description.lower()
            ][:self.page_size]
        
        self.display_packages()
    
    def display_packages(self):
        """Display current filtered packages"""
        # Update results counter
        result_count = len(self.displayed_packages)
        self.results_counter.setText(
            f"Found {result_count} package{'s' if result_count != 1 else ''}"
        )
        
        # Clear current list
        while self.packages_layout.count():
            item = self.packages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.displayed_packages:
            # Show no results message
            no_results = QLabel("No packages found 😔")
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
            
        # Add "Show More" button if needed
        total_packages = len(self.all_packages)
        displayed_count = len(self.displayed_packages)
        
        if displayed_count < total_packages and displayed_count < 1000:
            show_more = QPushButton("Show More")
            show_more.setStyleSheet(f"""
                QPushButton {{
                    font-family: {Fonts.DECORATIVE};
                    font-size: {Fonts.MEDIUM}px;
                    color: {ThemeColors.TEXT};
                    background: {ThemeColors.MEDIUM};
                    border: 3px solid {ThemeColors.LIGHT};
                    border-radius: 8px;
                    padding: 8px 25px;
                }}
                QPushButton:hover {{
                    background: {ThemeColors.LIGHT};
                    border-color: {ThemeColors.HIGHLIGHT};
                    color: {ThemeColors.HIGHLIGHT};
                }}
            """)
            show_more.clicked.connect(self.load_more_packages)
            self.packages_layout.addWidget(show_more)

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
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 8, 15, 8)

        # Package info with pixel border
        info = QLabel(f"📦 {pkg.name} (v{pkg.version})")
        if pkg.description:
            info.setToolTip(pkg.description)
        info.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.MEDIUM}px;
            color: {ThemeColors.TEXT};
            background: {ThemeColors.DARK};
            border: 2px solid {ThemeColors.LIGHT};
            border-radius: 4px;
            padding: 8px 15px;
        """)

        # Install button with highlight colors
        install_btn = QPushButton("⬇️ Install")
        install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        install_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.HIGHLIGHT};
                background: transparent;
                border: 3px solid {ThemeColors.HIGHLIGHT};
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
            }}
        """)

        layout.addWidget(info, stretch=1)
        layout.addWidget(install_btn)
        self.packages_layout.addWidget(item)

    def load_more_packages(self):
        """Load next page of packages"""
        self.current_page += 1
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.all_packages), 1000)
        self.displayed_packages = self.all_packages[:end_idx]
        self.display_packages()