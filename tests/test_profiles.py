"""Test suite for profile management"""
import unittest
import tempfile
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.profile_manager import (
    Profile, 
    ProfileService, 
    JsonProfileRepository,
    InvalidProfileError,
    ProfileAlreadyExistsError,
    ProfileNotFoundError
)


class TestProfile(unittest.TestCase):
    """Test Profile model"""
    
    def test_valid_profile_creation(self):
        """Test creating a valid profile"""
        profile = Profile(name="Test", username="Steve", ram=4)
        self.assertEqual(profile.name, "Test")
        self.assertEqual(profile.username, "Steve")
        self.assertEqual(profile.ram, 4)
    
    def test_invalid_profile_no_name(self):
        """Test profile creation fails without name"""
        with self.assertRaises(InvalidProfileError):
            Profile(name="", username="Steve", ram=4)
    
    def test_invalid_profile_no_username(self):
        """Test profile creation fails without username"""
        with self.assertRaises(InvalidProfileError):
            Profile(name="Test", username="", ram=4)
    
    def test_invalid_profile_invalid_ram(self):
        """Test profile creation fails with invalid RAM"""
        with self.assertRaises(InvalidProfileError):
            Profile(name="Test", username="Steve", ram=0)
    
    def test_profile_to_dict(self):
        """Test converting profile to dictionary"""
        profile = Profile(name="Test", username="Steve", ram=4, description="Test profile")
        data = profile.to_dict()
        
        self.assertEqual(data['name'], "Test")
        self.assertEqual(data['username'], "Steve")
        self.assertEqual(data['ram'], 4)
        self.assertEqual(data['description'], "Test profile")


class TestJsonProfileRepository(unittest.TestCase):
    """Test JSON repository"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name) / "profiles.json"
        self.repo = JsonProfileRepository(self.temp_path)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def test_load_empty_profiles(self):
        """Test loading default profiles"""
        profiles = self.repo.load()
        self.assertIn("default", profiles)
    
    def test_save_and_load_profiles(self):
        """Test saving and loading profiles"""
        profile = Profile(name="Test", username="Steve", ram=4)
        self.repo.save({"Test": profile})
        
        loaded = self.repo.load()
        self.assertIn("Test", loaded)
        self.assertEqual(loaded["Test"].username, "Steve")


class TestProfileService(unittest.TestCase):
    """Test profile service"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name) / "profiles.json"
        self.repo = JsonProfileRepository(self.temp_path)
        self.service = ProfileService(self.repo)
    
    def tearDown(self):
        """Clean-up"""
        self.temp_dir.cleanup()
    
    def test_create_profile(self):
        """Test creating a profile"""
        profile = self.service.create_profile("Vanilla", "Steve", 4)
        self.assertEqual(profile.name, "Vanilla")
    
    def test_create_duplicate_profile(self):
        """Test creating duplicate profile fails"""
        self.service.create_profile("Vanilla", "Steve", 4)
        
        with self.assertRaises(ProfileAlreadyExistsError):
            self.service.create_profile("Vanilla", "Alex", 8)
    
    def test_get_profile(self):
        """Test getting a profile"""
        self.service.create_profile("Vanilla", "Steve", 4)
        profile = self.service.get_profile("Vanilla")
        self.assertEqual(profile.username, "Steve")
    
    def test_get_nonexistent_profile(self):
        """Test getting nonexistent profile fails"""
        with self.assertRaises(ProfileNotFoundError):
            self.service.get_profile("NonExistent")
    
    def test_update_profile(self):
        """Test updating a profile"""
        self.service.create_profile("Vanilla", "Steve", 4)
        updated = self.service.update_profile("Vanilla", "Alex", 8)
        
        self.assertEqual(updated.username, "Alex")
        self.assertEqual(updated.ram, 8)
    
    def test_delete_profile(self):
        """Test deleting a profile"""
        self.service.create_profile("Vanilla", "Steve", 4)
        self.service.delete_profile("Vanilla")
        
        with self.assertRaises(ProfileNotFoundError):
            self.service.get_profile("Vanilla")
    
    def test_list_profiles(self):
        """Test listing profiles"""
        self.service.create_profile("Vanilla", "Steve", 4)
        self.service.create_profile("Modded", "Alex", 8)
        
        profiles = self.service.list_profiles()
        self.assertIn("Vanilla", profiles)
        self.assertIn("Modded", profiles)


if __name__ == '__main__':
    unittest.main()
