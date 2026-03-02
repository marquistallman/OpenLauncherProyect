"""Main application window"""
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from typing import Optional

from ..core.profile_manager import ProfileService, JsonProfileRepository, Profile
from ..core.minecraft_launcher import MinecraftManager
from ..core.mod_manager import ModManager
from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import MinecraftLaunchError
from .components import (
    ThemedFrame, ThemedLabel, ThemedButton,
    PlaceholderEntry, PlayButton, StatusBar
)
from .profile_dialogs import NewProfileDialog, EditProfileDialog, DeleteProfileDialog
from .version_manager_dialog import VersionManagerDialog
from .mod_manager_dialog import ModManagerDialog

logger = get_logger(__name__)


class ProfileSelector(ThemedFrame):
    """Widget for profile selection and management"""
    
    def __init__(
        self,
        master,
        profile_service: ProfileService,
        on_profile_changed: Optional[callable] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.profile_service = profile_service
        self.on_profile_changed = on_profile_changed
        
        self.selected_profile = StringVar(value=Config.DEFAULT_PROFILE_NAME)
        
        self._build_ui()
        self._refresh_profiles()
    
    def _build_ui(self) -> None:
        """Build selector UI"""
        label = ThemedLabel(self, text="Perfil:")
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.combo = ttk.Combobox(
            self,
            textvariable=self.selected_profile,
            state="readonly"
        )
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combo.bind("<<ComboboxSelected>>", self._on_profile_selected)
        
        self.new_btn = ThemedButton(self, text="+ New", width=8)
        self.new_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ThemedButton(self, text="Edit", width=8)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ThemedButton(self, text="Delete", width=8)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
    
    def _refresh_profiles(self) -> None:
        """Refresh profile list"""
        profiles = self.profile_service.list_profiles()
        self.combo['values'] = profiles
        
        if self.selected_profile.get() not in profiles:
            self.selected_profile.set(Config.DEFAULT_PROFILE_NAME)
    
    def _on_profile_selected(self, event) -> None:
        """Handle profile selection change"""
        if self.on_profile_changed:
            profile_name = self.selected_profile.get()
            profile = self.profile_service.get_profile(profile_name)
            self.on_profile_changed(profile)
    
    def get_selected_profile(self) -> Optional[Profile]:
        """Get currently selected profile"""
        profile_name = self.selected_profile.get()
        return self.profile_service.get_profile(profile_name)
    
    def show_new_dialog(self, parent) -> None:
        """Show new profile dialog"""
        def on_created(profile: Profile) -> None:
            self._refresh_profiles()
            self.selected_profile.set(profile.name)
        
        NewProfileDialog(parent, self.profile_service, on_created)
    
    def show_edit_dialog(self, parent) -> None:
        """Show edit profile dialog"""
        profile_name = self.selected_profile.get()
        
        def on_updated(profile: Profile) -> None:
            self._refresh_profiles()
        
        EditProfileDialog(parent, self.profile_service, profile_name, on_updated)
    
    def show_delete_dialog(self, parent) -> None:
        """Show delete profile dialog"""
        profile_name = self.selected_profile.get()
        
        def on_deleted(name: str) -> None:
            self._refresh_profiles()
            self.selected_profile.set(Config.DEFAULT_PROFILE_NAME)
        
        DeleteProfileDialog(parent, self.profile_service, profile_name, on_deleted)


class VersionSelector(ThemedFrame):
    """Widget for Minecraft version selection"""
    
    def __init__(self, master, minecraft_manager: MinecraftManager, **kwargs):
        super().__init__(master, **kwargs)
        self.minecraft_manager = minecraft_manager
        self.selected_version = StringVar()
        
        self._build_ui()
        self._refresh_versions()
    
    def _build_ui(self) -> None:
        """Build version selector UI"""
        label = ThemedLabel(self, text="Versión de Minecraft:")
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.combo = ttk.Combobox(
            self,
            textvariable=self.selected_version,
            state="readonly"
        )
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.refresh_btn = ThemedButton(self, text="Refresh", width=10)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        self.refresh_btn.config(command=self._refresh_versions)
    
    def _refresh_versions(self) -> None:
        """Refresh version list"""
        versions = self.minecraft_manager.version_manager.get_installed_versions()
        
        if not versions:
            versions = ["No versions installed"]
            self.combo.config(state="disabled")
        else:
            self.combo.config(state="readonly")
        
        self.combo['values'] = versions
        if versions:
            self.selected_version.set(versions[0])
    
    def get_selected_version(self) -> Optional[str]:
        """Get selected version"""
        version = self.selected_version.get()
        return version if version != "No versions installed" else None


class MainWindow(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title(Config.WINDOW_TITLE)
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.configure(bg=Config.COLORS['primary'])
        self.resizable(False, False)
        
        logger.info("Initializing main window")
        
        # Initialize services
        self.profile_service = ProfileService(JsonProfileRepository())
        self.minecraft_manager = MinecraftManager()
        self.mod_manager = ModManager()
        
        self._build_ui()
        self._check_prequisites()
    
    def _build_ui(self) -> None:
        """Build the main window UI"""
        # Header
        header = ThemedFrame(self, use_secondary=True)
        header.pack(fill=tk.X, pady=10)
        
        ThemedLabel(header, text=Config.APP_NAME, font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Main content
        content = ThemedFrame(self)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Profile section
        profile_label = ThemedLabel(content, text="Perfil", font=('Arial', 11, 'bold'))
        profile_label.pack(anchor='w', pady=(0, 5))
        
        self.profile_selector = ProfileSelector(
            content,
            self.profile_service,
            self._on_profile_changed
        )
        self.profile_selector.pack(fill=tk.X, pady=(0, 15))
        
        self.profile_selector.new_btn.config(
            command=lambda: self.profile_selector.show_new_dialog(self)
        )
        self.profile_selector.edit_btn.config(
            command=lambda: self.profile_selector.show_edit_dialog(self)
        )
        self.profile_selector.delete_btn.config(
            command=lambda: self.profile_selector.show_delete_dialog(self)
        )
        
        # Current profile info
        info_frame = ThemedFrame(content, use_secondary=True)
        info_frame.pack(fill=tk.X, pady=(0, 15), padx=10, ipady=10)
        
        ThemedLabel(info_frame, text="Usuario:", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.username_label = ThemedLabel(info_frame, text="")
        self.username_label.pack(anchor='w', padx=(20, 0))
        
        ThemedLabel(info_frame, text="RAM:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(5, 0))
        self.ram_label = ThemedLabel(info_frame, text="")
        self.ram_label.pack(anchor='w', padx=(20, 0))
        
        # Version section
        version_label = ThemedLabel(content, text="Versión", font=('Arial', 11, 'bold'))
        version_label.pack(anchor='w', pady=(15, 5))
        
        self.version_selector = VersionSelector(content, self.minecraft_manager)
        self.version_selector.pack(fill=tk.X, pady=(0, 20))
        
        # Quick entry fields (optional overrides)
        quick_label = ThemedLabel(content, text="Sobrescribir (opcional):", font=('Arial', 9))
        quick_label.pack(anchor='w', pady=(10, 5))
        
        quick_frame = ThemedFrame(content)
        quick_frame.pack(fill=tk.X, pady=(0, 15))
        
        ThemedLabel(quick_frame, text="Usuario:").pack(side=tk.LEFT, padx=(0, 5))
        self.quick_username = PlaceholderEntry(quick_frame, placeholder="Dejar vacío para usar perfil")
        self.quick_username.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ThemedLabel(quick_frame, text="RAM:").pack(side=tk.LEFT, padx=(0, 5))
        self.quick_ram = PlaceholderEntry(quick_frame, placeholder="GB")
        self.quick_ram.pack(side=tk.LEFT, expand=False, padx=(0, 10))
        
        # Managers section
        managers_label = ThemedLabel(content, text="Gestores", font=('Arial', 11, 'bold'))
        managers_label.pack(anchor='w', pady=(15, 5))
        
        managers_frame = ThemedFrame(content)
        managers_frame.pack(fill=tk.X, pady=(0, 20))
        
        version_mgr_btn = ThemedButton(
            managers_frame,
            text="📥 Versiones",
            command=lambda: VersionManagerDialog(self, self.minecraft_manager.version_manager, self._on_version_installed)
        )
        version_mgr_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        mod_mgr_btn = ThemedButton(
            managers_frame,
            text="🔍 Mods",
            command=lambda: ModManagerDialog(self, self.mod_manager, self._on_mod_installed)
        )
        mod_mgr_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Play button
        PlayButton(content, command=self._launch_game).pack(pady=20)
        
        # Status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _on_profile_changed(self, profile: Profile) -> None:
        """Handle profile selection change"""
        self.username_label.config(text=profile.username or "Sin especificar")
        self.ram_label.config(text=f"{profile.ram} GB")
        self.status_bar.set_status(f"Perfil '{profile.name}' seleccionado", "info")
    
    def _check_prequisites(self) -> None:
        """Check if prerequisites are met"""
        status = self.minecraft_manager.get_status()
        
        if not status['java_installed']:
            self.status_bar.set_status("⚠️ Java no instalado", "warning")
            logger.warning("Java not installed")
        
        if not status['installed_versions']:
            self.status_bar.set_status("⚠️ No hay versiones de Minecraft", "warning")
            logger.warning("No Minecraft versions installed")
        else:
            self.status_bar.set_status(f"Listo - {len(status['installed_versions'])} versiones disponibles", "success")
        
        logger.debug(f"Minecraft status: {status}")
    
    def _launch_game(self) -> None:
        """Launch Minecraft game"""
        try:
            # Get profile
            profile = self.profile_selector.get_selected_profile()
            if not profile:
                messagebox.showerror("Error", "Invalid profile")
                return
            
            # Get version
            version = self.version_selector.get_selected_version()
            if not version:
                messagebox.showerror("Error", "No Minecraft version selected")
                return
            
            # Check for quick overrides
            username = self.quick_username.get_clean()
            ram_str = self.quick_ram.get_clean()
            
            if username:
                profile.username = username
            
            if ram_str:
                try:
                    profile.ram = int(ram_str)
                except ValueError:
                    messagebox.showerror("Error", "RAM must be a valid number")
                    return
            
            # Launch
            self.status_bar.set_status("Lanzando juego...", "info")
            self.update()
            
            self.minecraft_manager.launcher.launch(profile, version, self._on_game_closed)
            
            logger.info(f"Game launched: {profile.username} on {version}")
        
        except MinecraftLaunchError as e:
            logger.error(f"Launch failed: {e}")
            self.status_bar.set_status("Error al lanzar el juego", "error")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logger.error(f"Unexpected error during launch: {e}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def _on_version_installed(self, version: str) -> None:
        """Called when a new version is installed"""
        logger.info(f"Version installed: {version}")
        self.version_selector._refresh_versions()
        self.status_bar.set_status(f"Versión {version} instalada", "success")
    
    def _on_mod_installed(self, mod_name: str) -> None:
        """Called when a mod is installed"""
        logger.info(f"Mod installed: {mod_name}")
        self.status_bar.set_status(f"Mod {mod_name} instalado", "success")
    
    def _on_game_closed(self) -> None:
        """Called when game closes"""
        logger.info("Game closed")
        self.status_bar.set_status("Juego cerrado", "info")


def run_application() -> None:
    """Run the application"""
    app = MainWindow()
    app.mainloop()
