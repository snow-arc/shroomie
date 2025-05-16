"""
Logger Module
Provides centralized logging functionality for the application.

Features:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- File and console output
- Custom formatting
- Log rotation
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config.app_config import Config

class Logger:
    """
    Custom logger configuration for the application.
    
    Provides formatted logging to both file and console with different
    levels of verbosity and automatic log rotation.
    """
    
    # Log format string
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Log file settings
    MAX_BYTES = 5 * 1024 * 1024  # 5MB
    BACKUP_COUNT = 3
    
    @classmethod
    def setup(cls, name="shroomie", level=logging.INFO):
        """
        Setup and configure the logger.
        
        Args:
            name (str): Logger name
            level (int): Logging level (e.g., logging.DEBUG)
            
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Create formatters and handlers
        formatter = logging.Formatter(cls.FORMAT)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler with rotation
        log_file = Config.BASE_DIR / "logs" / "shroomie.log"
        log_file.parent.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=cls.MAX_BYTES,
            backupCount=cls.BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name="shroomie"):
        """
        Get an existing logger or create a new one.
        
        Args:
            name (str): Logger name
            
        Returns:
            logging.Logger: Logger instance
        """
        return logging.getLogger(name)
