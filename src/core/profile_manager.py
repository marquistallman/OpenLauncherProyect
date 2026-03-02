"""Profile management module using SOLID principles"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import (
    ProfileNotFoundError, 
    ProfileAlreadyExistsError, 
    InvalidProfileError
)

logger = get_logger(__name__)


@dataclass
class Profile:
    """Profile model"""
    name: str
    username: str
    ram: int
    description: str = ""
    
    def __post_init__(self):
        """Validate profile data"""
        if not self.name or not isinstance(self.name, str):
            raise InvalidProfileError("Profile name must be a non-empty string")
        if not self.username or not isinstance(self.username, str):
            raise InvalidProfileError("Username must be a non-empty string")
        if not isinstance(self.ram, int) or self.ram < 1:
            raise InvalidProfileError("RAM must be a positive integer")
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Profile':
        """Create profile from dictionary"""
        return cls(
            name=data.get('name'),
            username=data.get('username'),
            ram=int(data.get('ram', Config.DEFAULT_RAM_GB)),
            description=data.get('description', '')
        )


class ProfileRepository(ABC):
    """Abstract repository for profile persistence"""
    
    @abstractmethod
    def load(self) -> Dict[str, Profile]:
        """Load all profiles"""
        pass
    
    @abstractmethod
    def save(self, profiles: Dict[str, Profile]) -> None:
        """Save profiles"""
        pass


class JsonProfileRepository(ProfileRepository):
    """JSON file repository implementation"""
    
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or Config.get_profiles_file()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict[str, Profile]:
        """Load profiles from JSON file"""
        try:
            if not self.file_path.exists():
                logger.info(f"Profiles file not found at {self.file_path}, creating default")
                return self._create_default_profiles()
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profiles = {}
            for name, profile_data in data.items():
                try:
                    profiles[name] = Profile.from_dict({**profile_data, 'name': name})
                except InvalidProfileError as e:
                    logger.error(f"Invalid profile '{name}': {e}")
            
            return profiles
        
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted profiles file: {e}")
            return self._create_default_profiles()
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
            return self._create_default_profiles()
    
    def save(self, profiles: Dict[str, Profile]) -> None:
        """Save profiles to JSON file"""
        try:
            data = {name: profile.to_dict() for name, profile in profiles.items()}
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Profiles saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Error saving profiles: {e}")
            raise
    
    def _create_default_profiles(self) -> Dict[str, Profile]:
        """Create default profile"""
        default_profile = Profile(
            name=Config.DEFAULT_PROFILE_NAME,
            username="",
            ram=Config.DEFAULT_RAM_GB
        )
        self.save({Config.DEFAULT_PROFILE_NAME: default_profile})
        return {Config.DEFAULT_PROFILE_NAME: default_profile}


class ProfileService:
    """Service for profile management (Business Logic)"""
    
    def __init__(self, repository: ProfileRepository):
        self.repository = repository
        self._profiles = self.repository.load()
    
    def create_profile(self, name: str, username: str, ram: int) -> Profile:
        """
        Create a new profile
        
        Args:
            name: Profile name
            username: Minecraft username
            ram: RAM allocation in GB
        
        Returns:
            Created Profile object
        
        Raises:
            ProfileAlreadyExistsError: If profile already exists
            InvalidProfileError: If profile data is invalid
        """
        if name in self._profiles:
            logger.warning(f"Attempted to create existing profile: {name}")
            raise ProfileAlreadyExistsError(f"Profile '{name}' already exists")
        
        profile = Profile(name=name, username=username, ram=ram)
        self._profiles[name] = profile
        self.repository.save(self._profiles)
        
        logger.info(f"Profile created: {name}")
        return profile
    
    def get_profile(self, name: str) -> Profile:
        """
        Get a profile by name
        
        Args:
            name: Profile name
        
        Returns:
            Profile object
        
        Raises:
            ProfileNotFoundError: If profile doesn't exist
        """
        if name not in self._profiles:
            logger.warning(f"Profile not found: {name}")
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        return self._profiles[name]
    
    def update_profile(self, name: str, username: str, ram: int, description: str = "") -> Profile:
        """
        Update an existing profile
        
        Args:
            name: Profile name
            username: Updated username
            ram: Updated RAM allocation
            description: Updated description
        
        Returns:
            Updated Profile object
        
        Raises:
            ProfileNotFoundError: If profile doesn't exist
            InvalidProfileError: If profile data is invalid
        """
        if name not in self._profiles:
            logger.warning(f"Attempted to update non-existent profile: {name}")
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        profile = Profile(name=name, username=username, ram=ram, description=description)
        self._profiles[name] = profile
        self.repository.save(self._profiles)
        
        logger.info(f"Profile updated: {name}")
        return profile
    
    def delete_profile(self, name: str) -> None:
        """
        Delete a profile
        
        Args:
            name: Profile name
        
        Raises:
            ProfileNotFoundError: If profile doesn't exist
        """
        if name == Config.DEFAULT_PROFILE_NAME:
            logger.warning("Attempted to delete default profile")
            raise ProfileException("Cannot delete default profile")
        
        if name not in self._profiles:
            logger.warning(f"Attempted to delete non-existent profile: {name}")
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        del self._profiles[name]
        self.repository.save(self._profiles)
        
        logger.info(f"Profile deleted: {name}")
    
    def list_profiles(self) -> List[str]:
        """Get list of all profile names"""
        return list(self._profiles.keys())
    
    def get_all_profiles(self) -> Dict[str, Profile]:
        """Get all profiles"""
        return self._profiles.copy()
    
    def refresh(self) -> None:
        """Refresh profiles from storage"""
        self._profiles = self.repository.load()
        logger.debug("Profiles refreshed from storage")


from ..utils.exceptions import ProfileException
