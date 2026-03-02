"""Version manager dialog"""
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional, Dict, List
import threading

from ..core.minecraft_launcher import MinecraftVersionManager
from ..utils.config import Config
from ..utils.logger import get_logger
from .components import ThemedFrame, ThemedLabel, ThemedButton, PlaceholderEntry

logger = get_logger(__name__)

CATEGORY_ICONS = {
    'Releases': '📦',
    'Snapshots': '📷',
    'Alphas': '🔬',
    'Betas': '🧪',
    'Classic': '🏛️',
    'Pre-releases': '⚠️'
}


class VersionManagerDialog(tk.Toplevel):
    """Dialog for managing Minecraft versions with categorization"""
    
    def __init__(
        self,
        parent,
        version_manager: MinecraftVersionManager,
        on_installed: Optional[Callable[[str], None]] = None
    ):
        super().__init__(parent)
        
        self.version_manager = version_manager
        self.on_installed = on_installed
        self.title("Gestor de Versiones")
        self.geometry("700x600")
        self.configure(bg=Config.COLORS['primary'])
        
        self.all_versions = []
        self.categorized_versions = {}
        self.installed_versions = []
        self.is_downloading = False
        self.search_query = ""
        self.selected_loader = tk.StringVar(value="vanilla")
        self.selected_loader_version = tk.StringVar(value="latest")
        
        self._build_ui()
        self._load_versions()
        self.center_on_parent(parent)
        self.grab_set()
    
    def _build_ui(self) -> None:
        """Build the dialog UI"""
        # Main frame
        content_frame = ThemedFrame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header
        header = ThemedFrame(content_frame, use_secondary=True)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        header_label = ThemedLabel(header, text="📥 Descargar Versiones", font=('Arial', 14, 'bold'))
        header_label.pack(pady=15, padx=15)
        
        # Divider
        divider = tk.Frame(content_frame, bg=Config.COLORS['accent'], height=2)
        divider.pack(fill=tk.X, pady=(0, 15))
        
        # Search frame
        search_frame = ThemedFrame(content_frame)
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        search_label = ThemedLabel(search_frame, text="🔍 Buscar versión:", font=('Arial', 10, 'bold'))
        search_label.pack(anchor='w', pady=(0, 8))
        
        search_input = ThemedFrame(search_frame)
        search_input.pack(fill=tk.X)
        
        self.search_entry = PlaceholderEntry(search_input, placeholder="Ej: 1.20, snapshot, alpha...")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', lambda e: self._filter_versions())
        
        clear_btn = ThemedButton(search_input, text="✕ Limpiar", command=lambda: self._clear_search(), width=10)
        clear_btn.pack(side=tk.LEFT)
        
        # Versions treeview frame
        versions_frame = ThemedFrame(content_frame)
        versions_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        versions_label = ThemedLabel(versions_frame, text="📦 Versiones Disponibles:", font=('Arial', 10, 'bold'))
        versions_label.pack(anchor='w', pady=(0, 8))
        
        # Treeview with scrollbar
        tree_frame = ThemedFrame(versions_frame, use_secondary=True)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12), padx=2, ipady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=scrollbar.set,
            height=16,
            show='tree'
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.tree.yview)
        
        # Configure treeview colors and fonts
        style = ttk.Style()
        style.configure('Treeview', 
                       background=Config.COLORS['secondary'], 
                       foreground=Config.COLORS['white'],
                       fieldbackground=Config.COLORS['secondary'],
                       font=('Arial', 9))
        style.configure('Treeview.Heading', 
                       background=Config.COLORS['accent'], 
                       foreground=Config.COLORS['white'],
                       font=('Arial', 9, 'bold'))
        style.map('Treeview', 
                 background=[('selected', Config.COLORS['accent'])])
        
        # Status label
        self.status_label = ThemedLabel(versions_frame, text="Cargando versiones...", font=('Arial', 9))
        self.status_label.pack(anchor='w', pady=(0, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            versions_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        
        # Loader selection frame
        loader_frame = ThemedFrame(content_frame)
        loader_frame.pack(fill=tk.X, padx=15, pady=(15, 0))
        
        loader_label = ThemedLabel(loader_frame, text="🔧 Tipo de Instalación:", font=('Arial', 10, 'bold'))
        loader_label.pack(anchor='w', pady=(0, 8))
        
        loader_options_frame = ThemedFrame(loader_frame)
        loader_options_frame.pack(fill=tk.X)
        
        tk.Radiobutton(
            loader_options_frame,
            text="📦 Vanilla",
            variable=self.selected_loader,
            value="vanilla",
            bg=Config.COLORS['primary'],
            fg=Config.COLORS['white'],
            selectcolor=Config.COLORS['accent'],
            activebackground=Config.COLORS['secondary'],
            activeforeground=Config.COLORS['white']
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Radiobutton(
            loader_options_frame,
            text="⚒️ Forge",
            variable=self.selected_loader,
            value="forge",
            bg=Config.COLORS['primary'],
            fg=Config.COLORS['white'],
            selectcolor=Config.COLORS['accent'],
            activebackground=Config.COLORS['secondary'],
            activeforeground=Config.COLORS['white']
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Radiobutton(
            loader_options_frame,
            text="🧵 Fabric",
            variable=self.selected_loader,
            value="fabric",
            bg=Config.COLORS['primary'],
            fg=Config.COLORS['white'],
            selectcolor=Config.COLORS['accent'],
            activebackground=Config.COLORS['secondary'],
            activeforeground=Config.COLORS['white']
        ).pack(side=tk.LEFT)
        
        # Buttons frame
        sep = tk.Frame(content_frame, bg=Config.COLORS['accent'], height=2)
        sep.pack(fill=tk.X, pady=(15, 0))
        
        button_frame = ThemedFrame(content_frame, use_secondary=True)
        button_frame.pack(fill=tk.X, padx=0, pady=0)
        
        self.download_btn = ThemedButton(button_frame, text="⬇️  Descargar", command=self._download_version, width=15)
        self.download_btn.pack(side=tk.LEFT, padx=8, pady=10, expand=True, fill=tk.BOTH)
        
        refresh_btn = ThemedButton(button_frame, text="🔄  Actualizar", command=self._load_versions, width=15)
        refresh_btn.pack(side=tk.LEFT, padx=8, pady=10, expand=True, fill=tk.BOTH)
        
        close_btn = ThemedButton(button_frame, text="✕  Cerrar", command=self.destroy, width=15)
        close_btn.pack(side=tk.LEFT, padx=8, pady=10, expand=True, fill=tk.BOTH)
    
    
    def _load_versions(self) -> None:
        """Load available versions in a separate thread"""
        self.status_label.config(text="Cargando versiones disponibles...")
        self.download_btn.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        
        def load_thread():
            try:
                self.all_versions = self.version_manager.get_available_versions()
                self.installed_versions = self.version_manager.get_installed_versions()
                self.categorized_versions = self.version_manager.categorize_versions(self.all_versions)
                
                self.after(0, self._populate_tree)
            except Exception as e:
                logger.error(f"Error loading versions: {e}")
                self.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))
        
        thread = threading.Thread(target=load_thread, daemon=True)
        thread.start()
    
    def _populate_tree(self) -> None:
        """Populate treeview with categorized versions"""
        self.tree.delete(*self.tree.get_children())
        
        total_versions = len(self.all_versions)
        installed_count = len(self.installed_versions)
        
        for category, versions in self.categorized_versions.items():
            if not versions:
                continue
            
            # Create category node
            icon = CATEGORY_ICONS.get(category, '📌')
            category_text = f"{icon} {category} ({len(versions)})"
            category_id = self.tree.insert('', 'end', text=category_text, open=False)
            
            # Add versions to category
            for version in versions:
                if version in self.installed_versions:
                    display = f"✓ {version}"
                else:
                    display = f"  {version}"
                self.tree.insert(category_id, 'end', text=display)
        
        self.status_label.config(
            text=f"✓ {installed_count} instaladas | 📥 {total_versions} disponibles"
        )
        self.download_btn.config(state=tk.NORMAL)
    
    def _filter_versions(self) -> None:
        """Filter versions based on search query"""
        self.search_query = self.search_entry.get_clean().lower()
        self.tree.delete(*self.tree.get_children())
        
        if not self.search_query:
            self._populate_tree()
            return
        
        # Filter and display matching versions
        matches_count = 0
        for category, versions in self.categorized_versions.items():
            matching_versions = [v for v in versions if self.search_query in v.lower()]
            
            if not matching_versions:
                continue
            
            matches_count += len(matching_versions)
            
            # Create category node
            icon = CATEGORY_ICONS.get(category, '📌')
            category_text = f"{icon} {category} ({len(matching_versions)})"
            category_id = self.tree.insert('', 'end', text=category_text, open=True)
            
            # Add matching versions
            for version in matching_versions:
                if version in self.installed_versions:
                    display = f"✓ {version}"
                else:
                    display = f"  {version}"
                self.tree.insert(category_id, 'end', text=display)
        
        self.status_label.config(text=f"Búsqueda: {matches_count} resultado(s) encontrado(s)")
    
    def _clear_search(self) -> None:
        """Clear search and show all versions"""
        self.search_entry.delete(0, tk.END)
        self.search_query = ""
        self._populate_tree()
    
    def _download_version(self) -> None:
        """Download selected version"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una versión para descargar")
            return
        
        selected_item = selection[0]
        version_text = self.tree.item(selected_item)['text']
        
        # Extract version name (remove icons and install marker)
        version = version_text.replace("✓ ", "").replace("  ", "").strip()
        
        # If it's a category, show warning
        if any(version.startswith(icon) for icon in CATEGORY_ICONS.values()):
            messagebox.showwarning("Advertencia", "Selecciona una versión específica, no una categoría")
            return
        
        if version in self.installed_versions:
            messagebox.showinfo("Información", f"La versión {version} ya está instalada")
            return
        
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        loader = self.selected_loader.get()
        loader_version = None if self.selected_loader_version.get() == "latest" else self.selected_loader_version.get()
        
        def download_thread():
            try:
                loader_text = loader.capitalize()
                self.status_label.config(text=f"Descargando {version} ({loader_text})...")
                self.after(0, lambda: self.progress_bar.pack(fill=tk.X, pady=(0, 5)))
                
                success = self.version_manager.download_version(
                    version,
                    loader=loader,
                    loader_version=loader_version
                )
                
                if success:
                    self.after(0, lambda: messagebox.showinfo("Éxito", f"Versión {version} ({loader_text}) descargada correctamente"))
                    
                    if self.on_installed:
                        self.on_installed(version)
                    
                    self.after(0, self._load_versions)
                else:
                    self.after(0, lambda: messagebox.showerror("Error", f"No se pudo descargar {version} ({loader_text})"))
            
            except Exception as e:
                logger.error(f"Download error: {e}")
                self.after(0, lambda: messagebox.showerror("Error", f"Error descargando: {str(e)}"))
            
            finally:
                self.is_downloading = False
                self.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
                self.after(0, lambda: self.progress_bar.pack_forget())
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def center_on_parent(self, parent) -> None:
        """Center dialog on parent window"""
        self.update_idletasks()
        parent.update_idletasks()
        
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        
        self.geometry(f"+{x}+{y}")

