"""
DevInfo Page Module
Displays information about the developer with enhanced typography and spacing.
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                            QScrollArea, QPushButton)
from PyQt6.QtCore import Qt
from utils.themes.colors import ThemeColors
from utils.themes.fonts import Fonts

class DevInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """Initialize and setup the UI components"""
        # Create scroll area for the entire content
        scroll = QScrollArea(self)
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
                background: rgba(124, 186, 255, 0.4);
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(124, 186, 255, 0.6);
            }
        """)
        
        # Main container for all content
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(45)  # Increased spacing between sections
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center all content

        # Create main title
        title = self.create_title_section()
        layout.addWidget(title)

        # Content sections with improved spacing
        sections = [
            ("🧑‍💻 Developer Profile", self.create_profile_section()),
            ("⚡ Technical Skills", self.create_skills_section()),
            ("💌 Contact Info", self.create_contact_section())
        ]

        # Add sections with separators
        for title_text, section in sections:
            section_container = QWidget()
            section_layout = QVBoxLayout(section_container)
            section_layout.setSpacing(25)
            section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Section title with pixel art styling
            title_label = QLabel(title_text)
            title_label.setStyleSheet(f"""
                font-family: 'Press Start 2P';
                font-size: 22px;
                color: {ThemeColors.HIGHLIGHT};
                padding: 15px 20px;
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-bottom: 4px solid {ThemeColors.LIGHT};
                border-right: 4px solid {ThemeColors.LIGHT};
                margin: 8px 0;
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Content container with enhanced hover effect
            content_container = QWidget()
            content_layout = QVBoxLayout(content_container)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_container.setStyleSheet(f"""
                QWidget {{
                    background: {ThemeColors.DARK};
                    border: 2px solid {ThemeColors.LIGHT};
                    border-bottom: 4px solid {ThemeColors.LIGHT};
                    border-right: 4px solid {ThemeColors.LIGHT};
                    padding: 25px;
                    margin: 10px 5px;
                    min-height: {350 if title_text == "🧑‍💻 Developer Profile" else 'auto'};
                    transition: all 0.2s ease;
                }}
                QWidget:hover {{
                    border-color: {ThemeColors.HIGHLIGHT};
                    border-bottom: 6px solid {ThemeColors.HIGHLIGHT};
                    border-right: 6px solid {ThemeColors.HIGHLIGHT};
                    background: {ThemeColors.MEDIUM};
                    transform: translateY(-3px);
                }}
            """)
            content_layout.addWidget(section)
            content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            section_layout.addWidget(title_label)
            section_layout.addWidget(content_container)
            
            # Add separator except for last section
            if section is not sections[-1][1]:
                separator = QWidget()
                separator.setFixedHeight(3)
                separator.setStyleSheet(f"""
                    background: linear-gradient(to right, 
                        transparent, 
                        {ThemeColors.LIGHT}, 
                        transparent
                    );
                    margin: 25px 100px;
                    border-radius: 1px;
                """)
                layout.addWidget(separator)
            
            layout.addWidget(section_container)

        layout.addStretch()
        scroll.setWidget(container)
        
        # Main layout just contains the scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def create_title_section(self):
        """Create the main title section"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.HIGHLIGHT};
                border-bottom: 6px solid {ThemeColors.HIGHLIGHT};
                border-right: 6px solid {ThemeColors.HIGHLIGHT};
                padding: 30px;
                margin: 10px 5px 30px 5px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(20)

        # Main title
        title = QLabel("SHROOMIE PROJECT")
        title.setStyleSheet(f"""
            font-family: 'Press Start 2P';
            font-size: 32px;
            color: {ThemeColors.HIGHLIGHT};
            padding: 20px;
            letter-spacing: 2px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("Package Management System")
        subtitle.setStyleSheet(f"""
            font-family: 'DotGothic16';
            font-size: 24px;
            color: {ThemeColors.ACCENT};
            letter-spacing: 1px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return container
    
    def create_profile_section(self):
        """Create the developer profile section"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(25)
        layout.setContentsMargins(10, 20, 10, 20)  # هوامش متوازنة
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # محاذاة للمنتصف

        # Profile text with improved formatting
        info_text = """echo 010000010111001001100011011010000010110000100000011000100111010001110111 | perl -lpe '$_=pack("B*",$_)' """

        info = QLabel(info_text)
        info.setStyleSheet(f"""
            font-family: 'DotGothic16';
            font-size: 18px;
            color: {ThemeColors.TEXT};
            line-height: 1.8;
            letter-spacing: 1px;
            padding: 10px;
        """)
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        return container
    
    def create_skills_section(self):
        """Create the skills showcase section"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        skills = [
            ("Linux Systems", 95),
            ("Python Development", 90),
            ("Package Management", 85),
            ("UI/UX Design", 80),
            ("System Architecture", 85)
        ]            # Skills container with enhanced pixel art styling
        skills_container = QWidget()
        skills_container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-bottom: 5px solid {ThemeColors.LIGHT};
                border-right: 5px solid {ThemeColors.LIGHT};
                padding: 25px 20px;
            }}
        """)
        skills_layout = QVBoxLayout(skills_container)
        skills_layout.setSpacing(15)
        layout.addWidget(skills_container)

        for skill, level in skills:
            skill_widget = QWidget()
            skill_widget.setStyleSheet(f"""
                QWidget {{
                    border: 2px solid {ThemeColors.LIGHT};
                    border-bottom: 4px solid {ThemeColors.LIGHT};
                    border-right: 4px solid {ThemeColors.LIGHT};
                    background: {ThemeColors.DARK};
                    padding: 12px;
                }}
                QWidget:hover {{
                    border-color: {ThemeColors.HIGHLIGHT};
                    background: {ThemeColors.MEDIUM};
                }}
            """)
            skill_layout = QVBoxLayout(skill_widget)  # Changed to VBoxLayout
            skill_layout.setSpacing(6)
            skill_layout.setContentsMargins(8, 8, 8, 8)

            # Skill name with pixel art design
            name = QLabel(skill)
            name.setStyleSheet(f"""
                font-family: 'Press Start 2P';
                font-size: 14px;
                color: {ThemeColors.HIGHLIGHT};
                padding: 4px;
            """)
            name.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Progress container
            progress_container = QWidget()
            progress_container_layout = QHBoxLayout(progress_container)
            progress_container_layout.setContentsMargins(0, 4, 0, 4)

            # Progress bar with enhanced pixel art style
            progress = QWidget()
            progress.setFixedHeight(24)
            progress.setStyleSheet(f"""
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-bottom: 3px solid {ThemeColors.LIGHT};
                border-right: 3px solid {ThemeColors.LIGHT};
                margin: 0;
            """)

            # Progress fill with enhanced pixel art style
            progress_width = progress.width() if progress.width() > 0 else 200
            fill = QWidget(progress)
            fill.setFixedWidth(int((progress_width - 10) * level / 100))  # Subtract padding to prevent overflow
            fill.setStyleSheet(f"""
                background: {ThemeColors.HIGHLIGHT};
                border: 1px solid {ThemeColors.ACCENT};
                margin: 3px;
            """)
            fill.setFixedHeight(16)

            # Percentage with pixel art style
            percent = QLabel(f"{level}%")
            percent.setStyleSheet(f"""
                font-family: 'Press Start 2P';
                font-size: 12px;
                color: {ThemeColors.HIGHLIGHT};
                background: {ThemeColors.DARK};
                border: 2px solid {ThemeColors.LIGHT};
                border-bottom: 3px solid {ThemeColors.LIGHT};
                border-right: 3px solid {ThemeColors.LIGHT};
                padding: 4px 8px;
            """)

            skill_layout.addWidget(name)
            
            progress_container_layout.addWidget(progress, stretch=1)
            progress_container_layout.addWidget(percent)
            skill_layout.addWidget(progress_container)
            
            skills_layout.addWidget(skill_widget)

        return container
    
    def create_contact_section(self):
        """Create the contact information section with enhanced 2D game style"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        contacts = [
            ("📧", "Email", "no need, dont try to contact me"),
            ("🌐", "GitHub", "@snow-arc"),
            ("💬", "Discord", "@snowancestor")
        ]

        # Improved container styling with game console look
        contacts_container = QWidget()
        contacts_container.setStyleSheet(f"""
            QWidget {{
                background: {ThemeColors.DARK};
                border: 3px solid {ThemeColors.LIGHT};
                border-radius: 12px;
                padding: 20px;
                margin: 5px;
            }}
        """)
        contacts_layout = QVBoxLayout(contacts_container)
        contacts_layout.setSpacing(15)
        layout.addWidget(contacts_container)

        for icon, platform, handle in contacts:
            # Game-style contact card
            contact_widget = QWidget()
            contact_widget.setStyleSheet(f"""
                QWidget {{
                    background: {ThemeColors.DARK};
                    border: 2px solid {ThemeColors.LIGHT};
                    border-bottom: 4px solid {ThemeColors.LIGHT};
                    border-right: 4px solid {ThemeColors.LIGHT};
                    border-radius: 8px;
                    margin: 4px;
                    padding: 8px;
                }}
                QWidget:hover {{
                    background: {ThemeColors.MEDIUM};
                    border-color: {ThemeColors.HIGHLIGHT};
                    border-bottom: 6px solid {ThemeColors.HIGHLIGHT};
                    border-right: 6px solid {ThemeColors.HIGHLIGHT};
                    margin-top: 2px;
                    margin-left: 2px;
                }}
            """)
            contact_layout = QVBoxLayout(contact_widget)
            contact_layout.setSpacing(8)
            contact_layout.setContentsMargins(12, 8, 12, 8)

            # Icon and platform in game-style header
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(10)

            # Platform icon with enhanced style
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(f"""
                font-size: 20px;
                color: {ThemeColors.HIGHLIGHT};
                padding: 4px;
            """)
            
            # Platform name with pixel font
            platform_label = QLabel(platform)
            platform_label.setStyleSheet(f"""
                font-family: 'Press Start 2P';
                font-size: 14px;
                color: {ThemeColors.HIGHLIGHT};
                padding: 4px;
            """)

            header_layout.addWidget(icon_label)
            header_layout.addWidget(platform_label)
            header_layout.addStretch()

            # Handle/value with decorative container
            value_container = QWidget()
            value_container.setStyleSheet(f"""
                QWidget {{
                    background: {ThemeColors.DARK};
                    border: 2px solid {ThemeColors.LIGHT};
                    border-radius: 6px;
                    padding: 8px;
                }}
                QWidget:hover {{
                    border-color: {ThemeColors.HIGHLIGHT};
                    background: {ThemeColors.MEDIUM};
                }}
            """)
            value_layout = QHBoxLayout(value_container)
            value_layout.setContentsMargins(8, 4, 8, 4)

            value = QLabel(handle)
            value.setStyleSheet(f"""
                font-family: 'DotGothic16';
                font-size: 16px;
                color: {ThemeColors.TEXT};
                padding: 2px;
            """)
            value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_layout.addWidget(value)

            contact_layout.addWidget(header)
            contact_layout.addWidget(value_container)
            contacts_layout.addWidget(contact_widget)

        return container
