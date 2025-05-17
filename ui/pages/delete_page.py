"""
Delete Page Module
Provides package removal functionality with search capabilities.

Features:
- Package search
- List of installed packages
- Safe package removal
"""

from typing import List, Dict, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, 
                            QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QLayoutItem)
from PyQt6.QtCore import Qt, QProcess
from models.package import Package
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts
from services.aur_storage import AurPackageStorage
from services.page_communicator import PageCommunicator

class DeletePage(QWidget):
    """Package deletion page with search functionality"""
    
    def __init__(self) -> None:
        super().__init__()
        self.communicator = PageCommunicator.instance()
        self.communicator.refreshNeeded.connect(self.refresh_packages)
        self.aur_storage = AurPackageStorage()
        self.process: QProcess | None = None
        
        # Load initial packages from storage
        self.refresh_packages()
        self.initUI()

    def initUI(self) -> None:
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
        
    def create_header(self) -> QWidget:
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
    
    def create_search_section(self) -> QWidget:
        """Create search and refresh section"""
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
        self.search_input.textChanged.connect(self.filter_packages)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 15px;
                min-height: 40px;
            }}
        """)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.manual_refresh)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.TEXT};
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
                padding: 8px 25px;
                min-width: 120px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.LIGHT};
                border-color: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.HIGHLIGHT};
            }}
        """)
        
        layout.addWidget(self.search_input, stretch=1)
        layout.addWidget(refresh_btn)
        
        return container

    def create_packages_section(self) -> QScrollArea:
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
    
    def filter_packages(self) -> None:
        """Filter packages based on search text"""
        search_text = self.search_input.text().lower()
        self.displayed_packages = [
            pkg for pkg in self.all_packages
            if search_text in pkg.name.lower()
        ]
        self.display_packages()
    
    def display_packages(self) -> None:
        """Display filtered packages in the list"""
        # Clear current list
        while self.packages_layout.count():
            item: QLayoutItem = self.packages_layout.takeAt(0)
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
    
    def add_package_item(self, pkg: Package) -> None:
        """Create and add a package item to the list"""
        item = QWidget()
        item.setMaximumHeight(80)  # Limit height
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
        info.setMaximumWidth(250)  # Limit width
        info.setWordWrap(True)
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
                border: 2px solid {ThemeColors.WARNING};
                border-radius: 4px;
                padding: 4px 12px;
                min-width: 90px;
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

    def delete_package(self, item: QWidget, package_name: str) -> None:
        """Handle package deletion"""
        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to remove {package_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # Show deletion dialog
            self.delete_dialog = QWidget()
            self.delete_dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.delete_dialog.setStyleSheet(f"""
                background: {ThemeColors.DARK};
                border: 4px solid {ThemeColors.WARNING};
                border-radius: 15px;
            """)
            
            dialog_layout = QVBoxLayout(self.delete_dialog)
            msg = QLabel(f"Removing {package_name}...")
            msg.setStyleSheet(f"""
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.MEDIUM}px;
                color: {ThemeColors.WARNING};
                padding: 5px;
                margin: 5px;
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 5px;
            """)
            msg.setWordWrap(True)
            msg.setMaximumWidth(300)
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dialog_layout.addWidget(msg)
            
            self.delete_dialog.setFixedSize(350, 150)
            self.delete_dialog.show()
            
            # Start deletion process
            self.process = QProcess()
            self.process.finished.connect(
                lambda: self.handle_deletion_complete(item, package_name)
            )
            self.process.start('yay', ['-Rdd', '--noconfirm', package_name])

    def manual_refresh(self) -> None:
        """Handle manual refresh request"""
        # First sync with system to get latest changes
        self.aur_storage.sync_with_system()
        # Then refresh the display
        self.refresh_packages()

    def refresh_packages(self) -> None:
        """Refresh package list from storage"""
        stored_packages = self.aur_storage.get_all_packages()
        self.all_packages = [
            Package(name, data["version"], data.get("description", ""))
            for name, data in stored_packages.items()
        ]
        self.displayed_packages = self.all_packages.copy()
        if hasattr(self, 'packages_layout'):
            self.display_packages()

    def handle_deletion_complete(self, item: QWidget, package_name: str) -> None:
        """Handle package deletion completion"""
        if self.process and self.process.exitCode() == 0:
            try:
                # Remove from storage
                self.aur_storage.remove_package(package_name)
                
                # Notify other pages to refresh
                self.communicator.packageDeleted.emit(package_name)
                self.communicator.request_refresh()
                
                # Update UI
                self.refresh_packages()
                
                # Close dialog
                if hasattr(self, 'delete_dialog'):
                    self.delete_dialog.close()
                    
                QMessageBox.information(self, "Success", f"{package_name} was successfully removed!")
            except Exception as e:
                print(f"Error completing deletion: {e}")
        else:
            error = self.process.readAllStandardError().data().decode()
            QMessageBox.critical(self, "Error", f"Failed to remove {package_name}\n{error}")
            if hasattr(self, 'delete_dialog'):
                self.delete_dialog.close()