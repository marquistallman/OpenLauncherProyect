"""Configuration module"""
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Application configuration singleton"""
    
    # Base paths
    HOME_DIR = Path.home()
    APP_DIR = HOME_DIR / ".freelauncher"
    DATA_DIR = APP_DIR / "data"
    PROFILES_DIR = DATA_DIR / "profiles"
    MODS_DIR = DATA_DIR / "mods"
    LOGS_DIR = APP_DIR / "logs"
    
    # Minecraft paths
    MINECRAFT_DIR = os.path.join(os.getenv("APPDATA"), ".minecraftLauncher")
    
    # Application info
    APP_NAME = "FreeLauncher"
    APP_VERSION = "2.0.0"
    
    # UI Configuration
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    WINDOW_TITLE = "FreeLauncher - Modern Minecraft Launcher"
    
    # Theme colors
    COLORS = {
        "primary": "#2c3e50",
        "secondary": "#34495e",
        "accent": "#3498db",
        "success": "#27ae60",
        "success_hover": "#219d54",
        "danger": "#e74c3c",
        "warning": "#f39c12",
        "white": "#ffffff",
        "grey": "#95a5a6"
    }
    
    # Default values
    DEFAULT_RAM_GB = 2
    DEFAULT_PROFILE_NAME = "default"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize configuration directories"""
        cls.APP_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        cls.MODS_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Ensure Minecraft directory exists
        os.makedirs(cls.MINECRAFT_DIR, exist_ok=True)
    
    @classmethod
    def get_profiles_file(cls) -> Path:
        """Get path to profiles JSON file"""
        return cls.DATA_DIR / "profiles.json"
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "paths": {
                "app_dir": str(cls.APP_DIR),
                "data_dir": str(cls.DATA_DIR),
                "minecraft_dir": cls.MINECRAFT_DIR,
            },
            "window": {
                "width": cls.WINDOW_WIDTH,
                "height": cls.WINDOW_HEIGHT,
            }
        }


# Initialize on import
Config.initialize()
