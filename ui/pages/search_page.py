"""
Search Page Module
Provides real-time package search functionality.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QScrollArea, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QProcess, pyqtSignal, QTimer
import pexpect
import sys
import subprocess
from models.package import Package
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts
from ui.dialogs.install_dialog import InstallDialog
from ui.dialogs.password_dialog import PasswordDialog
from services.aur_storage import AurPackageStorage
from services.auth_manager import AuthManager
from services.sudo_auth import SudoAuth
from services.page_communicator import PageCommunicator

class PackageProcess(QProcess):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.dialog = None
        
    def start_installation(self, pkg_name, is_official):
        """Start the installation process"""
        if is_official:
            self.start('sudo', ['pacman', '-S', '--noconfirm', pkg_name])
        else:
            self.start('yay', ['-S', '--noconfirm', pkg_name])

class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        self.sudo_auth = SudoAuth()
        self.communicator = PageCommunicator.instance()  # Use instance method
        
        if not self.sudo_auth.authenticate(self):
            sys.exit(1)
        
        self.page_size = 200
        self.current_page = 0
        self.aur_storage = AurPackageStorage()  # Move this up
        self.auth_manager = AuthManager()
        
        # Update and fetch packages
        self.update_package_database()
        self.all_packages = self.fetch_packages()
        self.displayed_packages = self.all_packages[:self.page_size]
        self.initUI()
        
        # Connect to signals
        self.communicator.packageDeleted.connect(self.handle_package_deleted)
        self.communicator.packageUpdated.connect(self.refresh_package_list)
        self.communicator.refreshNeeded.connect(self.refresh_packages)

    def update_package_database(self):
        """Update package database before fetching"""
        try:
            # Update official repos
            subprocess.run(['sudo', 'pacman', '-Sy'], check=True)
            # Update AUR
            subprocess.run(['yay', '-Sy'], check=True)
        except Exception as e:
            print(f"Error updating package database: {e}")
    
    def fetch_packages(self):
        """Fetch packages using yay command"""
        try:
            # Get installed packages first
            installed_packages = set(self.aur_storage.get_all_packages().keys())
            
            # Fetch all available packages
            result = subprocess.run(['yay', '-Ss'], 
                                 capture_output=True, 
                                 text=True,
                                 check=True)
            
            packages = []
            current_pkg = None
            
            for line in result.stdout.split('\n'):
                if not line:  # Skip empty lines
                    continue
                    
                if line.startswith('    '):  # Description line
                    if current_pkg and current_pkg.name not in installed_packages:
                        current_pkg.description = line.strip()
                else:
                    try:
                        parts = line.split('/')
                        if len(parts) >= 2:
                            repo_pkg = parts[1].split()
                            if len(repo_pkg) >= 2:
                                name = repo_pkg[0]
                                
                                # Skip if already installed
                                if name in installed_packages:
                                    current_pkg = None
                                    continue
                                    
                                version = repo_pkg[1]
                                repo = parts[0]
                                current_pkg = Package(name, version, repo)
                                packages.append(current_pkg)
                    except Exception as e:
                        print(f"Error parsing line '{line}': {e}")
                        current_pkg = None
                        continue
            
            return packages
            
        except subprocess.CalledProcessError as e:
            print(f"Error running yay: {e}")
            return []
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
        item = QWidget()
        item.setFixedHeight(80)  # ارتفاع ثابت أصغر
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Package info container
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(5, 2, 5, 2)
        info_layout.setSpacing(2)

        # Package name
        name_label = QLabel(pkg.name)
        name_label.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.SMALL}px;
            color: {ThemeColors.HIGHLIGHT};
            background: {ThemeColors.DARK};
            padding: 4px 8px;
            border-radius: 4px;
        """)
        name_label.setWordWrap(True)

        # Version info
        version_label = QLabel(f"Version: {pkg.version}")
        version_label.setStyleSheet(f"""
            font-family: {Fonts.DECORATIVE};
            font-size: {Fonts.SMALL}px;
            color: {ThemeColors.TEXT};
        """)

        info_layout.addWidget(name_label)
        info_layout.addWidget(version_label)

        # Install button
        install_btn = QPushButton("⬇️ Install")
        install_btn.setFixedSize(90, 40)  # حجم ثابت أصغر
        install_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {Fonts.DECORATIVE};
                font-size: {Fonts.SMALL}px;
                color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.HIGHLIGHT};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background: {ThemeColors.HIGHLIGHT};
                color: {ThemeColors.DARK};
            }}
        """)
        install_btn.clicked.connect(lambda: self.install_package(pkg))

        layout.addWidget(info_container, stretch=1)
        layout.addWidget(install_btn)
        
        # Container style
        item.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.MEDIUM};
                border: 2px solid {ThemeColors.LIGHT};
                border-radius: 8px;
            }}
            QWidget:hover {{
                border-color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
            }}
        """)
        
        self.packages_layout.addWidget(item)

    def install_package(self, pkg):
        """Install the selected package"""
        try:
            # Check if package is from official repos
            is_official = pkg.repo in ['core', 'extra']
            
            # Create and configure process
            self.install_process = PackageProcess(self)
            self.install_process.readyReadStandardOutput.connect(self.handle_process_output)
            self.install_process.finished.connect(
                lambda code, _: self.handle_installation_complete(code == 0, pkg)
            )
            
            # Show installation dialog
            self.install_dialog = InstallDialog(pkg.name, self)
            self.install_dialog.show()
            
            # Start installation with delay
            QTimer.singleShot(100, lambda: self.install_process.start_installation(pkg.name, is_official))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_process_output(self):
        """Handle process output in real-time"""
        if hasattr(self, 'install_process'):
            try:
                output = self.install_process.readAllStandardOutput().data().decode()
                print(output)  # For debugging
                
                if "error" in output.lower():
                    self.install_dialog.close()
                    QMessageBox.critical(self, "Installation Error", output)
                elif "successfully installed" in output.lower():
                    self.install_dialog.show_success()
            except Exception as e:
                print(f"Error handling output: {e}")
    
    def handle_installation_complete(self, success, pkg):
        """Handle installation completion"""
        if success:
            # Update AUR storage
            if pkg.repo not in ['core', 'extra']:
                self.aur_storage.update_package(
                    pkg.name,
                    pkg.version,
                    pkg.description
                )
            
            # Notify other pages to refresh
            self.communicator.packageInstalled.emit(pkg.name)
            self.communicator.request_refresh()
            
            # Update own display
            self.refresh_packages()
            
            self.install_dialog.show_success()
        else:
            QMessageBox.critical(self, "Installation Error", 
                               "Failed to install package")
            self.install_dialog.close()
                
        try:
            # Cleanup
            if hasattr(self, 'install_process'):
                self.install_process.deleteLater()
            if hasattr(self, 'install_dialog'):
                QTimer.singleShot(2000, self.install_dialog.close)
        except Exception as e:
            print(f"Error in installation completion: {e}")
            QMessageBox.critical(self, "Error", str(e))

    def refresh_packages(self):
        """Refresh package list"""
        self.all_packages = self.fetch_packages()
        self.displayed_packages = self.all_packages[:self.page_size]
        self.display_packages()

    def load_more_packages(self):
        """Load next page of packages"""
        self.current_page += 1
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.all_packages), 1000)
        self.displayed_packages = self.all_packages[:end_idx]
        self.display_packages()
    
    def handle_package_deleted(self, package_name):
        """Handle when a package is deleted"""
        try:
            self.refresh_package_list()
        except Exception as e:
            print(f"Error handling deleted package: {e}")
    
    def refresh_package_list(self):
        """Refresh the package list"""
        self.all_packages = self.fetch_packages()
        self.displayed_packages = self.all_packages[:self.page_size]
        self.display_packages()