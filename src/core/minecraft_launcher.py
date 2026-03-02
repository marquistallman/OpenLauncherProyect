"""Minecraft launcher module"""
import subprocess
import os
import hashlib
from typing import List, Callable, Optional

import minecraft_launcher_lib

from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import MinecraftLaunchError, MinecraftVersionNotFoundError
from .profile_manager import Profile

logger = get_logger(__name__)


class MinecraftVersionManager:
    """Manages Minecraft versions"""
    
    def __init__(self, minecraft_dir: str = Config.MINECRAFT_DIR):
        self.minecraft_dir = minecraft_dir
    
    def get_installed_versions(self) -> List[str]:
        """
        Get list of installed Minecraft versions
        
        Returns:
            List of version strings
        """
        try:
            versions = minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_dir)
            version_ids = [v['id'] for v in versions]
            
            if not version_ids:
                logger.warning("No Minecraft versions found")
                return []
            
            logger.debug(f"Found {len(version_ids)} installed versions")
            return version_ids
        
        except Exception as e:
            logger.error(f"Error getting installed versions: {e}")
            return []
    
    def verify_version_installation(self, version: str) -> bool:
        """
        Verify if a specific version is installed
        
        Args:
            version: Version string to check
        
        Returns:
            True if version exists
        """
        return version in self.get_installed_versions()


class JavaVerifier:
    """Verifies Java installation"""
    
    @staticmethod
    def is_java_installed() -> bool:
        """Check if Java is installed"""
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Error checking Java installation: {e}")
            return False
    
    @staticmethod
    def get_java_version() -> Optional[str]:
        """Get Java version string"""
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stderr.split('\n')[0] if result.stderr else None
        except Exception as e:
            logger.warning(f"Error getting Java version: {e}")
            return None


class MinecraftLauncher:
    """Launches Minecraft game"""
    
    def __init__(self, minecraft_dir: str = Config.MINECRAFT_DIR):
        self.minecraft_dir = minecraft_dir
        self.version_manager = MinecraftVersionManager(minecraft_dir)
        self.java_verifier = JavaVerifier()
    
    def launch(
        self,
        profile: Profile,
        version: str,
        on_close: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Launch Minecraft with given profile
        
        Args:
            profile: Profile with username and RAM settings
            version: Minecraft version to launch
            on_close: Optional callback when game closes
        
        Raises:
            MinecraftLaunchError: If launch fails
        """
        try:
            # Verify prerequisites
            self._verify_prerequisites(version)
            
            # Build launch options
            options = self._build_launch_options(profile)
            
            logger.info(f"Launching Minecraft {version} with profile '{profile.name}'")
            
            # Get launch command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                version,
                self.minecraft_dir,
                options
            )
            
            # Execute
            process = subprocess.Popen(
                command,
                cwd=self.minecraft_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Execute callback when close is requested
            if on_close:
                on_close()
            
            logger.info(f"Minecraft process started with PID {process.pid}")
        
        except Exception as e:
            logger.error(f"Error launching Minecraft: {e}")
            raise MinecraftLaunchError(f"Failed to launch Minecraft: {str(e)}")
    
    def _verify_prerequisites(self, version: str) -> None:
        """Verify that prerequisites are met"""
        if not self.java_verifier.is_java_installed():
            raise MinecraftLaunchError("Java is not installed or not in PATH")
        
        if not self.version_manager.verify_version_installation(version):
            raise MinecraftVersionNotFoundError(f"Minecraft version '{version}' is not installed")
    
    def _build_launch_options(self, profile: Profile) -> dict:
        """Build options dict for launcher"""
        uuid = self._generate_offline_uuid(profile.username)
        
        return {
            'username': profile.username,
            'uuid': uuid,
            'token': '',
            'jvArguments': [
                f"-Xms{profile.ram}G",
                f"-Xmx{profile.ram}G",
            ],
            'launcherVersion': Config.APP_VERSION
        }
    
    @staticmethod
    def _generate_offline_uuid(username: str) -> str:
        """Generate offline UUID for player"""
        data = f"OfflinePlayer:{username}".encode('utf-8')
        md5_hash = hashlib.md5(data).hexdigest()
        
        # Format as UUID
        return f"{md5_hash[:8]}-{md5_hash[8:12]}-{md5_hash[12:16]}-{md5_hash[16:20]}-{md5_hash[20:]}"


class MinecraftManager:
    """Facade combining version and launcher management"""
    
    def __init__(self, minecraft_dir: str = Config.MINECRAFT_DIR):
        self.minecraft_dir = minecraft_dir
        self.launcher = MinecraftLauncher(minecraft_dir)
        self.version_manager = MinecraftVersionManager(minecraft_dir)
        self.java_verifier = JavaVerifier()
    
    def get_status(self) -> dict:
        """Get current Minecraft setup status"""
        return {
            'java_installed': self.java_verifier.is_java_installed(),
            'java_version': self.java_verifier.get_java_version(),
            'installed_versions': self.version_manager.get_installed_versions(),
            'minecraft_dir': self.minecraft_dir
        }
