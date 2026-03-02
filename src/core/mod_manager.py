"""Mod management module"""
import os
import requests
from typing import List, Dict, Optional
from pathlib import Path

from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import ModException

logger = get_logger(__name__)

MODRINTH_API = "https://api.modrinth.com/v2"


class ModSearchResult:
    """Represents a mod search result"""
    
    def __init__(self, data: dict):
        self.project_id = data.get('project_id')
        self.name = data.get('title')
        self.description = data.get('description')
        self.downloads = data.get('downloads', 0)
        self.followers = data.get('followers', 0)
        self.icon_url = data.get('icon_url')
    
    def __str__(self) -> str:
        return f"{self.name} ({self.downloads} downloads)"


class ModDownloader:
    """Handles mod downloading from Modrinth"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def search(self, query: str, limit: int = 10) -> List[ModSearchResult]:
        """
        Search for mods by name
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            List of ModSearchResult objects
        """
        try:
            url = f"{MODRINTH_API}/search"
            params = {
                'query': query,
                'limit': limit,
                'facets': '[[\"project_type:\"mod\"]]'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            results = [ModSearchResult(hit) for hit in data.get('hits', [])]
            
            logger.debug(f"Found {len(results)} mods for query '{query}'")
            return results
        
        except requests.RequestException as e:
            logger.error(f"Error searching mods: {e}")
            raise ModException(f"Failed to search mods: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error searching mods: {e}")
            raise ModException(f"Unexpected error: {str(e)}")
    
    def get_versions(self, project_id: str, minecraft_version: str) -> List[dict]:
        """
        Get compatible versions for a mod
        
        Args:
            project_id: Modrinth project ID
            minecraft_version: Minecraft version string
        
        Returns:
            List of version dictionaries
        """
        try:
            url = f"{MODRINTH_API}/project/{project_id}/version"
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            versions = response.json()
            compatible = [
                v for v in versions
                if minecraft_version in v.get('game_versions', [])
            ]
            
            logger.debug(f"Found {len(compatible)} compatible versions for {project_id}")
            return compatible
        
        except requests.RequestException as e:
            logger.error(f"Error getting mod versions: {e}")
            raise ModException(f"Failed to get mod versions: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error getting versions: {e}")
            raise ModException(f"Unexpected error: {str(e)}")
    
    def download_file(self, url: str, output_path: str) -> bool:
        """
        Download a file from URL
        
        Args:
            url: File URL
            output_path: Where to save file
        
        Returns:
            True if successful
        """
        try:
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify file was created
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise ModException(f"Failed to download {url}")
            
            logger.debug(f"Downloaded: {os.path.basename(output_path)}")
            return True
        
        except requests.RequestException as e:
            logger.error(f"Error downloading file: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading file: {e}")
            return False


class ModManager:
    """Manages mod installation and removal"""
    
    def __init__(self, mods_dir: Optional[str] = None):
        self.mods_dir = Path(mods_dir or Config.MODS_DIR)
        self.downloader = ModDownloader()
        self.mods_dir.mkdir(parents=True, exist_ok=True)
    
    def list_installed_mods(self) -> List[str]:
        """Get list of installed mod files"""
        try:
            return [f for f in os.listdir(self.mods_dir) if f.endswith('.jar')]
        except Exception as e:
            logger.error(f"Error listing mods: {e}")
            return []
    
    def install_mod(self, project_id: str, minecraft_version: str) -> bool:
        """
        Install a mod from Modrinth
        
        Args:
            project_id: Modrinth project ID
            minecraft_version: Target Minecraft version
        
        Returns:
            True if successful
        """
        try:
            versions = self.downloader.get_versions(project_id, minecraft_version)
            
            if not versions:
                logger.warning(f"No compatible versions for {project_id}")
                return False
            
            # Get latest version
            latest = versions[0]
            file_info = latest['files'][0]
            
            url = file_info['url']
            filename = file_info['filename']
            output_path = os.path.join(self.mods_dir, filename)
            
            if os.path.exists(output_path):
                logger.info(f"Mod already installed: {filename}")
                return True
            
            success = self.downloader.download_file(url, output_path)
            
            if success:
                logger.info(f"Mod installed: {filename}")
            
            return success
        
        except ModException as e:
            logger.error(f"Error installing mod: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error installing mod: {e}")
            return False
    
    def remove_mod(self, filename: str) -> bool:
        """
        Remove an installed mod
        
        Args:
            filename: Mod filename
        
        Returns:
            True if successful
        """
        try:
            mod_path = self.mods_dir / filename
            
            if not mod_path.exists():
                logger.warning(f"Mod not found: {filename}")
                return False
            
            os.remove(mod_path)
            logger.info(f"Mod removed: {filename}")
            return True
        
        except Exception as e:
            logger.error(f"Error removing mod: {e}")
            return False
