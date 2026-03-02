"""Profile management dialogs"""
import tkinter as tk
from tkinter import Toplevel, messagebox, ttk
from typing import Callable, Optional, List

from ..core.profile_manager import Profile, ProfileService
from ..utils.exceptions import (
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
    InvalidProfileError
)
from ..utils.config import Config
from ..utils.logger import get_logger
from .components import ThemedFrame, ThemedLabel, ThemedButton, PlaceholderEntry

logger = get_logger(__name__)


class ProfileDialog(Toplevel):
    """Base dialog for profile operations"""
    
    def __init__(self, parent, title: str = "Profile Dialog"):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x200")
        self.configure(bg=Config.COLORS['primary'])
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
    
    def center_on_parent(self) -> None:
        """Center dialog on parent window"""
        self.update_idletasks()
        parent = self.master
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class NewProfileDialog(ProfileDialog):
    """Dialog for creating a new profile"""
    
    def __init__(
        self,
        parent,
        profile_service: ProfileService,
        on_created: Optional[Callable[[Profile], None]] = None
    ):
        super().__init__(parent, "Create New Profile")
        self.profile_service = profile_service
        self.on_created = on_created
        self.created_profile: Optional[Profile] = None
        
        self._build_ui()
        self.center_on_parent()
    
    def _build_ui(self) -> None:
        """Build the dialog UI"""
        # Frame for inputs
        frame = ThemedFrame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Profile name
        ThemedLabel(frame, text="Profile Name:").pack(anchor='w', pady=(0, 5))
        self.name_entry = PlaceholderEntry(frame, placeholder="e.g., Vanilla")
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Username
        ThemedLabel(frame, text="Minecraft Username:").pack(anchor='w', pady=(0, 5))
        self.username_entry = PlaceholderEntry(frame, placeholder="e.g., Steve")
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # RAM
        ThemedLabel(frame, text="RAM (GB):").pack(anchor='w', pady=(0, 5))
        self.ram_var = tk.StringVar(value=str(Config.DEFAULT_RAM_GB))
        ram_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=32,
            textvariable=self.ram_var,
            bg=Config.COLORS['secondary'],
            fg=Config.COLORS['white']
        )
        ram_spinbox.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = ThemedFrame(self)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ThemedButton(button_frame, text="Create", command=self._create_profile).pack(side=tk.LEFT, padx=5)
        ThemedButton(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def _create_profile(self) -> None:
        """Create the profile"""
        try:
            name = self.name_entry.get_clean().strip()
            username = self.username_entry.get_clean().strip()
            ram = int(self.ram_var.get())
            
            # Validate inputs
            if not name:
                messagebox.showwarning("Validation Error", "Please enter a profile name")
                return
            
            if not username:
                messagebox.showwarning("Validation Error", "Please enter a username")
                return
            
            if ram < 1 or ram > 32:
                messagebox.showwarning("Validation Error", "RAM must be between 1 and 32 GB")
                return
            
            # Create profile
            profile = self.profile_service.create_profile(name, username, ram)
            self.created_profile = profile
            
            logger.info(f"Profile created: {name}")
            
            if self.on_created:
                self.on_created(profile)
            
            messagebox.showinfo("Success", f"Profile '{name}' created successfully")
            self.destroy()
        
        except ProfileAlreadyExistsError:
            messagebox.showerror("Error", "A profile with that name already exists")
        except InvalidProfileError as e:
            messagebox.showerror("Validation Error", str(e))
        except ValueError:
            messagebox.showerror("Validation Error", "RAM must be a valid number")
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            messagebox.showerror("Error", f"Failed to create profile: {str(e)}")


class EditProfileDialog(ProfileDialog):
    """Dialog for editing an existing profile"""
    
    def __init__(
        self,
        parent,
        profile_service: ProfileService,
        profile_name: str,
        on_updated: Optional[Callable[[Profile], None]] = None
    ):
        super().__init__(parent, f"Edit Profile: {profile_name}")
        self.profile_service = profile_service
        self.profile_name = profile_name
        self.on_updated = on_updated
        self.updated_profile: Optional[Profile] = None
        
        self._build_ui()
        self.center_on_parent()
    
    def _build_ui(self) -> None:
        """Build the dialog UI"""
        # Get current profile
        try:
            profile = self.profile_service.get_profile(self.profile_name)
        except ProfileNotFoundError:
            messagebox.showerror("Error", "Profile not found")
            self.destroy()
            return
        
        # Frame for inputs
        frame = ThemedFrame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Username
        ThemedLabel(frame, text="Minecraft Username:").pack(anchor='w', pady=(0, 5))
        self.username_entry = PlaceholderEntry(frame)
        self.username_entry.set_text(profile.username)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # RAM
        ThemedLabel(frame, text="RAM (GB):").pack(anchor='w', pady=(0, 5))
        self.ram_var = tk.StringVar(value=str(profile.ram))
        ram_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=32,
            textvariable=self.ram_var,
            bg=Config.COLORS['secondary'],
            fg=Config.COLORS['white']
        )
        ram_spinbox.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        ThemedLabel(frame, text="Description (optional):").pack(anchor='w', pady=(0, 5))
        self.description_entry = PlaceholderEntry(frame)
        self.description_entry.set_text(profile.description)
        self.description_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = ThemedFrame(self)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ThemedButton(button_frame, text="Save", command=self._update_profile).pack(side=tk.LEFT, padx=5)
        ThemedButton(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def _update_profile(self) -> None:
        """Update the profile"""
        try:
            username = self.username_entry.get_clean().strip()
            ram = int(self.ram_var.get())
            description = self.description_entry.get_clean().strip()
            
            # Validate inputs
            if not username:
                messagebox.showwarning("Validation Error", "Please enter a username")
                return
            
            if ram < 1 or ram > 32:
                messagebox.showwarning("Validation Error", "RAM must be between 1 and 32 GB")
                return
            
            # Update profile
            profile = self.profile_service.update_profile(
                self.profile_name,
                username,
                ram,
                description
            )
            self.updated_profile = profile
            
            logger.info(f"Profile updated: {self.profile_name}")
            
            if self.on_updated:
                self.on_updated(profile)
            
            messagebox.showinfo("Success", "Profile updated successfully")
            self.destroy()
        
        except InvalidProfileError as e:
            messagebox.showerror("Validation Error", str(e))
        except ValueError:
            messagebox.showerror("Validation Error", "RAM must be a valid number")
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")


class DeleteProfileDialog(ProfileDialog):
    """Dialog for confirming profile deletion"""
    
    def __init__(
        self,
        parent,
        profile_service: ProfileService,
        profile_name: str,
        on_deleted: Optional[Callable[[str], None]] = None
    ):
        super().__init__(parent, f"Delete Profile")
        self.profile_service = profile_service
        self.profile_name = profile_name
        self.on_deleted = on_deleted
        
        if profile_name == Config.DEFAULT_PROFILE_NAME:
            messagebox.showerror("Error", "Cannot delete the default profile")
            self.destroy()
            return
        
        self._build_ui()
        self.center_on_parent()
    
    def _build_ui(self) -> None:
        """Build the dialog UI"""
        # Frame for text
        frame = ThemedFrame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Confirmation message
        message = f"Are you sure you want to delete profile '{self.profile_name}'?\nThis action cannot be undone."
        ThemedLabel(frame, text=message, wraplength=300, justify=tk.LEFT).pack(pady=10)
        
        # Buttons
        button_frame = ThemedFrame(self)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        delete_btn = ThemedButton(button_frame, text="Delete")
        delete_btn.config(bg=Config.COLORS['danger'])
        delete_btn.config(command=self._confirm_delete)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        ThemedButton(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def _confirm_delete(self) -> None:
        """Confirm and delete the profile"""
        try:
            self.profile_service.delete_profile(self.profile_name)
            
            logger.info(f"Profile deleted: {self.profile_name}")
            
            if self.on_deleted:
                self.on_deleted(self.profile_name)
            
            messagebox.showinfo("Success", "Profile deleted successfully")
            self.destroy()
        
        except ProfileNotFoundError:
            messagebox.showerror("Error", "Profile not found")
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            messagebox.showerror("Error", f"Failed to delete profile: {str(e)}")
