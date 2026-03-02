"""Logging module"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import Config


class Logger:
    """Centralized logging configuration"""
    
    _instance: Optional['Logger'] = None
    _loggers: dict = {}
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize logging system"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Create log file handler
        log_file = Config.LOGS_DIR / f"freelauncher_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(detailed_formatter)
        
        # Store handlers for reuse
        self._file_handler = file_handler
        self._console_handler = console_handler
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger with the given name"""
        logger = logging.getLogger(name)
        
        if name not in cls._loggers:
            logger.setLevel(logging.DEBUG)
            logger.addHandler(cls()._file_handler)
            logger.addHandler(cls()._console_handler)
            cls._loggers[name] = logger
        
        return logger


# Convenience function
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return Logger.get_logger(name)
