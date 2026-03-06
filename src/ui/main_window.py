"""Main application window"""
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from typing import Optional
import threading

from ..core.profile_manager import ProfileService, JsonProfileRepository, Profile
from ..core.minecraft_launcher import MinecraftManager
from ..core.mod_manager import ModManager
from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import MinecraftLaunchError
from .components import (
    ThemedFrame, ThemedLabel, ThemedButton,
    PlaceholderEntry, PlayButton, StatusBar, ScrollableFrame
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
        label = ThemedLabel(self, text="👤 Perfil:", font=('Segoe UI', 11, 'bold'))
        label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.combo = ttk.Combobox(
            self,
            textvariable=self.selected_profile,
            state="readonly",
            font=('Segoe UI', 10)
        )
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combo.bind("<<ComboboxSelected>>", self._on_profile_selected)
        
        self.new_btn = ThemedButton(self, text="➕ Nuevo", width=10)
        self.new_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ThemedButton(self, text="✏️ Editar", width=10)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ThemedButton(self, text="🗑️ Eliminar", width=10)
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
        label = ThemedLabel(self, text="🎯 Versión:", font=('Segoe UI', 11, 'bold'))
        label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.combo = ttk.Combobox(
            self,
            textvariable=self.selected_version,
            state="readonly",
            font=('Segoe UI', 10)
        )
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.refresh_btn = ThemedButton(self, text="🔄 Actualizar", width=15)
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
        self.resizable(True, True)
        
        logger.info("Initializing main window")
        
        # Initialize services
        self.profile_service = ProfileService(JsonProfileRepository())
        self.minecraft_manager = MinecraftManager()
        self.mod_manager = ModManager()
        
        self._build_ui()
        self._check_prequisites()
    
    def _build_ui(self) -> None:
        """Build the main window UI"""
        # Header with improved visual
        header = ThemedFrame(self, use_secondary=True)
        header.pack(fill=tk.X, pady=0)
        
        header_inner = ThemedFrame(header)
        header_inner.pack(padx=20, pady=20)
        
        title_label = ThemedLabel(header_inner, text="🎮 " + Config.APP_NAME, font=('Segoe UI', 22, 'bold'))
        title_label.pack(pady=(0, 5))
        
        subtitle = ThemedLabel(header_inner, text="Modern Minecraft Launcher", font=('Segoe UI', 11), fg=Config.COLORS['grey'])
        subtitle.pack()
        
        # Main content with scrolling capability
        scrollable_content = ScrollableFrame(self, bg=Config.COLORS['primary'])
        scrollable_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        content = scrollable_content.scrollable_frame
        
        # Profile section with improved styling
        profile_label = ThemedLabel(content, text="👤 PERFIL", font=('Segoe UI', 12, 'bold'))
        profile_label.pack(anchor='w', pady=(0, 10), padx=5)
        
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
        
        # Current profile info with better layout
        info_frame = ThemedFrame(content, use_secondary=True)
        info_frame.pack(fill=tk.X, pady=(0, 20), padx=12, ipady=15)
        
        # User info on one line
        user_inner = ThemedFrame(info_frame)
        user_inner.pack(fill=tk.X, pady=(0, 10))
        
        ThemedLabel(user_inner, text="📛 Usuario:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.username_label = ThemedLabel(user_inner, text="", font=('Segoe UI', 10))
        self.username_label.pack(side=tk.LEFT, expand=True)
        
        # RAM info on one line
        ram_inner = ThemedFrame(info_frame)
        ram_inner.pack(fill=tk.X)
        
        ThemedLabel(ram_inner, text="💾 RAM:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.ram_label = ThemedLabel(ram_inner, text="", font=('Segoe UI', 10))
        self.ram_label.pack(side=tk.LEFT, expand=True)
        
        # Version section
        version_label = ThemedLabel(content, text="🎯 VERSIÓN DE MINECRAFT", font=('Segoe UI', 12, 'bold'))
        version_label.pack(anchor='w', pady=(20, 10), padx=5)
        
        self.version_selector = VersionSelector(content, self.minecraft_manager)
        self.version_selector.pack(fill=tk.X, pady=(0, 20))
        
        # Quick entry fields (optional overrides)
        quick_label = ThemedLabel(content, text="⚙️ OPCIONES AVANZADAS (OPCIONAL)", font=('Segoe UI', 12, 'bold'))
        quick_label.pack(anchor='w', pady=(15, 10), padx=5)
        
        quick_frame = ThemedFrame(content, use_secondary=True)
        quick_frame.pack(fill=tk.X, pady=(0, 20), padx=12, ipady=12)
        
        # User override
        user_override_frame = ThemedFrame(quick_frame)
        user_override_frame.pack(fill=tk.X, pady=(0, 10))
        ThemedLabel(user_override_frame, text="Usuario:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.quick_username = PlaceholderEntry(quick_frame, placeholder="Dejar vacío para usar el del perfil")
        self.quick_username.pack(fill=tk.X, padx=(0, 0), pady=(0, 10))
        
        # RAM override
        ram_override_frame = ThemedFrame(quick_frame)
        ram_override_frame.pack(fill=tk.X, pady=(0, 0))
        ThemedLabel(ram_override_frame, text="RAM:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.quick_ram = PlaceholderEntry(quick_frame, placeholder="GB (dejar vacío para usar el del perfil)")
        self.quick_ram.pack(fill=tk.X)
        
        # Managers section with improved layout
        managers_label = ThemedLabel(content, text="🛠️ GESTORES", font=('Segoe UI', 12, 'bold'))
        managers_label.pack(anchor='w', pady=(20, 10), padx=5)
        
        managers_frame = ThemedFrame(content)
        managers_frame.pack(fill=tk.X, pady=(0, 25))
        
        version_mgr_btn = ThemedButton(
            managers_frame,
            text="📥  Descargar Versiones",
            command=lambda: VersionManagerDialog(self, self.minecraft_manager.version_manager, self._on_version_installed)
        )
        version_mgr_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        mod_mgr_btn = ThemedButton(
            managers_frame,
            text="🔍  Gestor de Mods",
            command=lambda: ModManagerDialog(self, self.mod_manager, self._on_mod_installed)
        )
        mod_mgr_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Play button - bigger and more prominent
        play_button = PlayButton(content, command=self._launch_game)
        play_button.pack(pady=(30, 10), fill=tk.X, padx=80)
        
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
            
            # Launch in separate thread to avoid blocking UI
            self.status_bar.set_status("Lanzando juego...", "info")
            self.update()
            
            def launch_thread():
                try:
                    self.minecraft_manager.launcher.launch(profile, version)
                    self.after(0, lambda: self._on_game_closed())
                except MinecraftLaunchError as e:
                    logger.error(f"Launch failed: {e}")
                    self.after(0, lambda: self.status_bar.set_status("Error al lanzar el juego", "error"))
                    self.after(0, lambda: messagebox.showerror("Error", str(e)))
                except Exception as e:
                    logger.error(f"Unexpected error during launch: {e}")
                    self.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))
            
            thread = threading.Thread(target=launch_thread, daemon=True)
            thread.start()
            
            logger.info(f"Game launched: {profile.username} on {version}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
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
