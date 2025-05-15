# Font configuration
PIXEL_FONTS = {
    'primary': 'PixelifySans',
    'secondary': 'DotGothic16',
    'decorative': 'Press Start 2P'
}

# Default to system fonts as fallback
FONT_FAMILY = f"{PIXEL_FONTS['primary']}, {PIXEL_FONTS['secondary']}, {PIXEL_FONTS['decorative']}, monospace"

# Theme colors
dark_theme = {
    "background": "#1a1528",    # Deep purple background
    "dark": "#2a1f3d",          # Rich purple
    "medium": "#3d2a5c",        # Mystic purple
    "light": "#4e357c",         # Twilight purple
    "text": "#ffe1ff",          # Soft pink text
    "highlight": "#ff7cba",     # Electric pink highlight
    "accent": "#e839d8",        # Cyber pink
    "warning": "#ff6b6b",       # Neon red
    "success": "#bb00ff",       # Magic purple
    "pixel_border": "#4e357c"   # Twilight border
}

light_theme = {
    "background": "#fff0f5",    # Soft pink background
    "dark": "#f8e1ff",          # Pale purple
    "medium": "#ffcef4",        # Light pink
    "light": "#ffffff",         # White
    "text": "#2a1f3d",          # Rich purple text
    "highlight": "#ff7cba",     # Electric pink highlight
    "accent": "#e839d8",        # Cyber pink accent
    "warning": "#ff6b6b",       # Coral warning
    "success": "#bb00ff",       # Magic purple
    "pixel_border": "#ff7cba"   # Electric pink border
}

# Default to dark theme
colors = dark_theme.copy()

# Define the font family to use throughout the app
FONT_FAMILY = "'DotGothic16', 'PixelifySans', 'Press Start 2P', sans-serif"

sidebar_style = f"""
    QWidget {{
        background: {colors['dark']};
        border-right: 4px solid {colors['pixel_border']};
        border-bottom: 4px solid {colors['pixel_border']};
        padding: 12px;
        background-image: linear-gradient(
            to bottom,
            {colors['dark']},
            {colors['medium']} 120%
        );
    }}
    
    QPushButton[class="nav-button"] {{
        font-family: {PIXEL_FONTS['decorative']};
        font-size: 16px;
        color: {colors['text']};
        background: {colors['dark']};
        border: 2px solid {colors['light']};
        border-bottom: 4px solid {colors['light']};
        border-right: 4px solid {colors['light']};
        padding: 12px 15px;
        margin: 8px 4px;
        text-align: left;
        min-width: 160px;
    }}
    
    QPushButton[class="nav-button"]:hover {{
        background: {colors['medium']};
        border-color: {colors['highlight']};
        color: {colors['highlight']};
        transform: translateX(3px);
    }}
    
    QPushButton[class="nav-button"]:pressed {{
        background: {colors['highlight']};
        color: {colors['dark']};
        border-bottom: 2px solid {colors['light']};
        border-right: 2px solid {colors['light']};
    }}
    
    QLabel[class="pixel-divider"] {{
        min-height: 4px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 transparent,
            stop:0.4 {colors['light']},
            stop:0.6 {colors['light']},
            stop:1 transparent
        );
        margin: 15px 5px;
    }}
"""

button_style = f"""
    QPushButton {{
        font-family: {PIXEL_FONTS['decorative']};
        font-size: 16px;
        color: {colors['text']};
        background: {colors['dark']};
        border: 4px solid {colors['light']};
        border-radius: 6px;
        padding: 15px;
        margin: 6px;
        text-align: center;
        min-width: 180px;
        min-height: 50px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    QPushButton:hover {{
        background: {colors['medium']};
        border-color: {colors['highlight']};
        color: {colors['highlight']};
        transform: scale(1.05);
    }}
    QPushButton:pressed {{
        background: {colors['highlight']};
        color: {colors['dark']};
        border-color: {colors['accent']};
        transform: scale(0.95);
    }}
"""

package_style = f"""
    QWidget {{
        background: {colors['medium']};
        border: 3px solid {colors['light']};
        border-radius: 8px;
        padding: 12px;
        margin: 6px;
        min-height: 50px;
    }}
    QWidget:hover {{
        border-color: {colors['highlight']};
        background: {colors['dark']};
        transform: scale(1.02);
    }}
    QLabel {{
        font-family: {PIXEL_FONTS['decorative']};
        color: {colors['text']};
        font-size: 14px;
        letter-spacing: 1px;
    }}
    QLabel[class="package-name"] {{
        color: {colors['highlight']};
        font-size: 16px;
        letter-spacing: 2px;
        padding: 4px;
    }}
"""

search_input_style = f"""
    QLineEdit {{
        font-family: {PIXEL_FONTS['decorative']};
        font-size: 14px;
        color: {colors['text']};
        background: {colors['dark']};
        border: 3px solid {colors['light']};
        border-radius: 6px;
        padding: 12px;
        margin: 4px;
        letter-spacing: 1px;
    }}
    QLineEdit:focus {{
        border-color: {colors['highlight']};
        background: {colors['medium']};
    }}
"""

search_button_style = f"""
    QPushButton {{
        {button_style}
        min-width: 100px;
    }}
"""

page_title_style = f"""
    font-family: {FONT_FAMILY};
    font-size: 24px;
    color: {colors['highlight']};
    margin: 20px;
"""

download_card_style = f"""
    QWidget {{
        background: {colors['medium']};
        border: 2px solid {colors['light']};
        border-radius: 8px;
        padding: 15px;
    }}
    QLabel {{
        font-family: {FONT_FAMILY};
        font-size: 14px;
        color: {colors['text']};
    }}
"""