"""
Theme Colors Module
Defines enhanced color schemes for the application.

Features:
- Vibrant but eye-friendly color palette
- Consistent color harmony
- Clear contrast ratios
- Semantic color naming
"""

class ThemeColors:
    """Application theme color definitions with enhanced visual harmony."""
    
    # Dark theme with magical purple colors
    DARK_THEME = {
        'background': "#1a1528",    # Deep purple background
        'dark': "#2a1f3d",          # Rich purple
        'medium': "#3d2a5c",        # Mystic purple
        'light': "#4e357c",         # Twilight purple
        'text': "#ffe1ff",          # Soft pink text
        'highlight': "#ff7cba",     # Electric pink highlight
        'accent': "#e839d8",        # Cyber pink
        'warning': "#ff6b6b",       # Neon red
        'success': "#bb00ff",       # Magic purple
        'pixel_border': "#ff7cba"   # Electric pink border
    }
    
    # Light theme with soft pink contrast
    LIGHT_THEME = {
        'background': "#fff0f5",    # Soft pink background
        'dark': "#ffd4e3",          # Gentle pink
        'medium': "#ffb8d1",        # Light pink
        'light': "#ffffff",         # Pure white
        'text': "#3d2a5c",          # Mystic purple text
        'highlight': "#4e357c",     # Twilight purple highlight
        'accent': "#e839d8",        # Cyber pink accent
        'warning': "#ff6b6b",       # Soft red warning
        'success': "#bb00ff",       # Magic purple success
        'pixel_border': "#4e357c"   # Twilight purple border
    }
    
    # Initialize with dark theme and set as class variables
    BACKGROUND = DARK_THEME['background']
    DARK = DARK_THEME['dark']
    MEDIUM = DARK_THEME['medium']
    LIGHT = DARK_THEME['light']
    TEXT = DARK_THEME['text']
    HIGHLIGHT = DARK_THEME['highlight']
    ACCENT = DARK_THEME['accent']
    WARNING = DARK_THEME['warning']
    SUCCESS = DARK_THEME['success']
    PIXEL_BORDER = DARK_THEME['pixel_border']
    
    # Ensure initial theme is properly set
    @classmethod
    def init_theme(cls):
        """Initialize the default dark theme"""
        cls.set_theme(is_dark=True)
    
    @classmethod
    def set_theme(cls, is_dark=True):
        """Update color values based on selected theme."""
        theme = cls.DARK_THEME if is_dark else cls.LIGHT_THEME
        
        cls.BACKGROUND = theme['background']
        cls.DARK = theme['dark']
        cls.MEDIUM = theme['medium']
        cls.LIGHT = theme['light']
        cls.TEXT = theme['text']
        cls.HIGHLIGHT = theme['highlight']
        cls.ACCENT = theme['accent']
        cls.WARNING = theme['warning']
        cls.SUCCESS = theme['success']
        cls.PIXEL_BORDER = theme['pixel_border']
    
    @classmethod
    def get_color(cls, name, is_dark=True):
        """Get a specific color by name for the specified theme."""
        theme = cls.DARK_THEME if is_dark else cls.LIGHT_THEME
        return theme.get(name, cls.DARK_THEME['text'])
