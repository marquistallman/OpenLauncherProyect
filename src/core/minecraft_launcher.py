"""Minecraft launcher module"""
import subprocess
import os
import hashlib
from typing import List, Callable, Optional, Dict
import requests

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
    
    def get_available_versions(self) -> List[str]:
        """
        Get list of available Minecraft versions to download
        
        Returns:
            List of available version strings
        """
        try:
            index = minecraft_launcher_lib.utils.get_version_list()
            # index can be either a dict with 'versions' key or a list directly
            if isinstance(index, dict) and 'versions' in index:
                return [v['id'] for v in index['versions']]
            elif isinstance(index, list):
                return [v['id'] for v in index]
            else:
                logger.warning("Unexpected version list format")
                return []
        except Exception as e:
            logger.error(f"Error fetching available versions: {e}")
            return []
    
    def get_available_versions_with_dates(self) -> List[Dict]:
        """
        Get list of available Minecraft versions with release dates
        
        Returns:
            List of dicts with 'id', 'time', and 'type' keys
        """
        try:
            index = minecraft_launcher_lib.utils.get_version_list()
            versions = []
            
            if isinstance(index, dict) and 'versions' in index:
                versions = index['versions']
            elif isinstance(index, list):
                versions = index
            
            return versions if versions else []
        except Exception as e:
            logger.error(f"Error fetching available versions: {e}")
            return []
    
    
    def categorize_versions(self, versions: List[str]) -> dict:
        """
        Categorize versions by type (Release, Snapshot, Alpha, Classic, etc.)
        Sorted by release date (newest first)
        
        Args:
            versions: List of version strings
        
        Returns:
            Dict with categories as keys and version lists as values (sorted by date)
        """
        try:
            # Get version info with dates
            versions_info = self.get_available_versions_with_dates()
            version_dates = {v['id']: v.get('time', '') for v in versions_info}
            
            categories = {
                'Releases': [],
                'Snapshots': [],
                'Pre-releases': [],
                'Alphas': [],
                'Betas': [],
                'Classic': []
            }
            
            for version in versions:
                # Snapshots: YYwWWx format (e.g., 23w45a, 24w01a)
                if len(version) >= 5 and version[0:2].isdigit() and 'w' in version[2:4]:
                    categories['Snapshots'].append(version)
                # Pre-releases: X.Y.Z-pre/rc format
                elif '-pre' in version or '-rc' in version:
                    categories['Pre-releases'].append(version)
                # Alphas: a + version
                elif version.startswith('a'):
                    categories['Alphas'].append(version)
                # Betas: b + version
                elif version.startswith('b'):
                    categories['Betas'].append(version)
                # Classic: c + version
                elif version.startswith('c') or version.startswith('classic'):
                    categories['Classic'].append(version)
                # Releases: X.Y or X.Y.Z format (all digits and dots)
                elif all(c.isdigit() or c == '.' for c in version):
                    categories['Releases'].append(version)
            
            # Sort each category by release date (descending - newest first)
            def sort_by_date(version_list):
                try:
                    return sorted(
                        version_list,
                        key=lambda v: version_dates.get(v, '0000-00-00T00:00:00Z'),
                        reverse=True
                    )
                except Exception as e:
                    logger.warning(f"Error sorting versions: {e}")
                    return version_list
            
            for category in categories.keys():
                categories[category] = sort_by_date(categories[category])
            
            return categories
        except Exception as e:
            logger.error(f"Error categorizing versions: {e}")
            # Fallback to old behavior if something goes wrong
            categories = {
                'Releases': [],
                'Snapshots': [],
                'Pre-releases': [],
                'Alphas': [],
                'Betas': [],
                'Classic': []
            }
            
            for version in versions:
                if len(version) >= 5 and version[0:2].isdigit() and 'w' in version[2:4]:
                    categories['Snapshots'].append(version)
                elif '-pre' in version or '-rc' in version:
                    categories['Pre-releases'].append(version)
                elif version.startswith('a'):
                    categories['Alphas'].append(version)
                elif version.startswith('b'):
                    categories['Betas'].append(version)
                elif version.startswith('c') or version.startswith('classic'):
                    categories['Classic'].append(version)
                elif all(c.isdigit() or c == '.' for c in version):
                    categories['Releases'].append(version)
            
            for category in categories.values():
                category.sort(reverse=True)
            
            return categories
    
    
    def download_version(
        self,
        version: str,
        loader: str = "vanilla",
        loader_version: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """
        Download and install a specific Minecraft version
        
        Args:
            version: Version to download
            loader: Type of loader ('vanilla', 'forge', 'fabric')
            loader_version: Specific loader version (optional)
            progress_callback: Optional callback(downloaded, total) for progress tracking
        
        Returns:
            True if successful
        """
        try:
            loader_lower = loader.lower()
            logger.info(f"Starting download of Minecraft {version} with {loader_lower}")
            
            if loader_lower == "vanilla":
                # Download vanilla version directly
                logger.info(f"Installing vanilla Minecraft {version}")
                minecraft_launcher_lib.install.install_minecraft_version(version, self.minecraft_dir)
                logger.info(f"Successfully installed vanilla {version}")
            
            elif loader_lower == "forge":
                # Download Forge version
                try:
                    logger.info(f"Installing Forge for Minecraft {version}")
                    # Use find_forge_version to get the correct Forge version
                    forge_ver = minecraft_launcher_lib.forge.find_forge_version(version)
                    minecraft_launcher_lib.forge.install_forge_version(forge_ver, self.minecraft_dir)
                    logger.info(f"Successfully installed Forge for {version}")
                except Exception as forge_error:
                    logger.error(f"Forge installation failed: {forge_error}")
                    raise
            
            elif loader_lower == "fabric":
                # Install Fabric using the library method
                try:
                    logger.info(f"Installing Fabric for Minecraft {version}")
                    minecraft_launcher_lib.fabric.install_fabric(version, self.minecraft_dir)
                    
                    # Also download Fabric API mod
                    logger.info("Downloading Fabric API...")
                    self._download_fabric_api(version)
                    
                    logger.info(f"Successfully installed Fabric for {version}")
                except Exception as fabric_error:
                    logger.error(f"Fabric installation failed: {fabric_error}")
                    raise
            
            else:
                logger.error(f"Unknown loader type: {loader}")
                return False
            
            logger.info(f"Successfully downloaded Minecraft {version} with {loader_lower}")
            return True
        
        except Exception as e:
            logger.error(f"Error downloading version {version}: {e}")
            return False
    
    def _download_fabric_api(self, minecraft_version: str) -> None:
        """
        Download Fabric API mod from Modrinth
        
        Args:
            minecraft_version: Minecraft version for the API
        """
        try:
            # Check internet connection first
            requests.get("https://api.modrinth.com", timeout=5)
            
            # Create mods directory
            mods_dir = os.path.join(self.minecraft_dir, "mods")
            os.makedirs(mods_dir, exist_ok=True)
            
            # Get Fabric API from Modrinth (P7dR8mSH is the Fabric API project ID)
            url = "https://api.modrinth.com/v2/project/P7dR8mSH/version"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            fabric_api_url = None
            filename = None
            
            # Find the version that matches our Minecraft version
            for v in response.json():
                if minecraft_version in v.get("game_versions", []):
                    fabric_api_url = v["files"][0]["url"]
                    filename = v["files"][0]["filename"]
                    break
            
            if fabric_api_url and filename:
                logger.info(f"Downloading Fabric API: {filename}")
                fabric_api_path = os.path.join(mods_dir, filename)
                
                # Download the file
                api_response = requests.get(fabric_api_url, timeout=30)
                api_response.raise_for_status()
                
                with open(fabric_api_path, "wb") as f:
                    f.write(api_response.content)
                
                logger.info(f"Fabric API installed: {filename}")
            else:
                logger.warning(f"Fabric API not available for Minecraft {minecraft_version}")
        
        except requests.ConnectionError:
            logger.error("No internet connection to download Fabric API")
        except Exception as e:
            logger.warning(f"Could not download Fabric API: {e}")
    
    
    def get_forge_versions(self, minecraft_version: str) -> List[str]:
        """
        Get available Forge versions for a Minecraft version
        
        Args:
            minecraft_version: Minecraft version
        
        Returns:
            List of Forge versions
        """
        try:
            if hasattr(minecraft_launcher_lib, 'forge') and hasattr(minecraft_launcher_lib.forge, 'list_forge_versions'):
                versions = minecraft_launcher_lib.forge.list_forge_versions(minecraft_version)
                return versions if versions else []
            else:
                logger.warning("Forge version listing not supported in minecraft_launcher_lib")
                return []
        except Exception as e:
            logger.warning(f"Error getting Forge versions: {e}")
            return []
    
    def get_fabric_versions(self, minecraft_version: str) -> List[str]:
        """
        Get available Fabric loader versions for a Minecraft version
        
        Args:
            minecraft_version: Minecraft version
        
        Returns:
            List of Fabric versions
        """
        try:
            response = requests.get(
                f"https://meta.fabricmc.net/v2/versions/loader/{minecraft_version}",
                timeout=10
            )
            response.raise_for_status()
            loaders = response.json()
            return [loader['loader']['version'] for loader in loaders] if loaders else []
        except Exception as e:
            logger.warning(f"Error getting Fabric versions: {e}")
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
            on_close: Optional callback when game closes (deprecated, not used)
        
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
            
            logger.info(f"Running command: {' '.join(command)}")
            
            # Execute game - launcher stays open
            subprocess.run(command, cwd=self.minecraft_dir)
            
            logger.info("Minecraft process completed")
        
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
