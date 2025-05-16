"""
Font Configuration Module
Defines typography settings for the application.

This module manages:
- Font family definitions
- Font size constants
- Typography utility functions
- Font style generation
"""

class Fonts:
    """
    Static font definitions for the application.
    
    This class centralizes all font-related settings to ensure
    consistent typography across the application interface.
    
    Font Categories:
    - PRIMARY: Main text font (PixelifySans)
    - SECONDARY: Alternative text font (DotGothic16)
    - DECORATIVE: Pixel art styled font (Press Start 2P)
    - FALLBACK: System font fallback (monospace)
    """
    
    # Font families
    PRIMARY = 'PixelifySans'
    SECONDARY = 'DotGothic16'
    DECORATIVE = 'Press Start 2P'
    FALLBACK = 'monospace'
    
    # Font sizes (in pixels)
    TINY = 10
    SMALL = 12
    MEDIUM = 14
    LARGE = 16
    XLARGE = 24
    HUGE = 32
    
    # Line heights
    LINE_HEIGHT_NORMAL = 1.2
    LINE_HEIGHT_RELAXED = 1.5
    LINE_HEIGHT_LOOSE = 2.0
    
    # Letter spacing
    LETTER_SPACING_TIGHT = 0
    LETTER_SPACING_NORMAL = 1
    LETTER_SPACING_WIDE = 2
    
    # Font weights (where supported)
    WEIGHT_NORMAL = 400
    WEIGHT_BOLD = 700
    
    # Complete font family string with fallbacks
    FONT_FAMILY = f"{PRIMARY}, {SECONDARY}, {DECORATIVE}, {FALLBACK}"
    
    @classmethod
    def get_style(cls, size=MEDIUM, family=PRIMARY, color=None, weight=None,
                  letter_spacing=None, line_height=None):
        """
        Generate a complete font style string.
        
        Args:
            size (int): Font size in pixels
            family (str): Font family name
            color (str, optional): Text color
            weight (int, optional): Font weight
            letter_spacing (int, optional): Letter spacing in pixels
            line_height (float, optional): Line height multiplier
            
        Returns:
            str: Complete font style string
        """
        style = [f"font-family: {family}",
                f"font-size: {size}px"]
        
        if color:
            style.append(f"color: {color}")
        if weight:
            style.append(f"font-weight: {weight}")
        if letter_spacing:
            style.append(f"letter-spacing: {letter_spacing}px")
        if line_height:
            style.append(f"line-height: {line_height}")
        
        return "; ".join(style) + ";"
    
    @classmethod
    def get_title_style(cls, color=None):
        """
        Get a predefined style for titles.
        
        Args:
            color (str, optional): Text color
            
        Returns:
            str: Title style string
        """
        return cls.get_style(
            size=cls.XLARGE,
            family=cls.DECORATIVE,
            color=color,
            letter_spacing=cls.LETTER_SPACING_WIDE,
            line_height=cls.LINE_HEIGHT_RELAXED
        )
    
    @classmethod
    def get_button_style(cls, color=None):
        """
        Get a predefined style for buttons.
        
        Args:
            color (str, optional): Text color
            
        Returns:
            str: Button style string
        """
        return cls.get_style(
            size=cls.LARGE,
            family=cls.DECORATIVE,
            color=color,
            letter_spacing=cls.LETTER_SPACING_NORMAL
        )
