"""FreeLauncher - Modern Minecraft Launcher
Main entry point for the application
"""
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.utils.config import Config
from src.utils.logger import get_logger
from src.ui.main_window import run_application

logger = get_logger(__name__)


def main():
    """Main entry point"""
    try:
        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
        logger.info(f"Configuration: {Config.to_dict()}")
        
        run_application()
    
    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()


