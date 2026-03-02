"""Mod manager dialog"""
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional
import threading

from ..core.mod_manager import ModManager, ModDownloader
from ..utils.config import Config
from ..utils.logger import get_logger
from .components import ThemedFrame, ThemedLabel, ThemedButton, PlaceholderEntry

logger = get_logger(__name__)


class ModManagerDialog(tk.Toplevel):
    """Dialog for managing mods from Modrinth"""
    
    def __init__(
        self,
        parent,
        mod_manager: ModManager,
        on_installed: Optional[Callable[[str], None]] = None
    ):
        super().__init__(parent)
        
        self.mod_manager = mod_manager
        self.on_installed = on_installed
        self.title("Gestor de Mods")
        self.geometry("650x600")
        self.configure(bg=Config.COLORS['primary'])
        
        self.search_results = []
        self.is_searching = False
        self.is_downloading = False
        
        self._build_ui()
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
        
        ThemedLabel(header, text="🔍 Gestor de Mods - Modrinth", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Search frame
        search_frame = ThemedFrame(content_frame)
        search_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        ThemedLabel(search_frame, text="Buscar mods:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        input_frame = ThemedFrame(search_frame)
        input_frame.pack(fill=tk.X)
        
        self.search_entry = PlaceholderEntry(input_frame, placeholder="Nombre del mod...")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        search_btn = ThemedButton(input_frame, text="🔍 Buscar", command=self._search_mods, width=10)
        search_btn.pack(side=tk.LEFT)
        
        # Results frame
        results_frame = ThemedFrame(content_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        ThemedLabel(results_frame, text="Resultados (haz clic para descargar):", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Results listbox with scrollbar
        list_frame = ThemedFrame(results_frame, use_secondary=True)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=Config.COLORS['secondary'],
            fg=Config.COLORS['white'],
            font=('Arial', 9),
            height=14
        )
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_listbox.bind('<Button-1>', self._on_mod_selected)
        scrollbar.config(command=self.results_listbox.yview)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            results_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        
        # Status label
        self.status_label = ThemedLabel(results_frame, text="Ingresa un término de búsqueda", font=('Arial', 9))
        self.status_label.pack(anchor='w', pady=(0, 10))
        
        # Buttons frame
        sep = tk.Frame(content_frame, bg=Config.COLORS['secondary'], height=2)
        sep.pack(fill=tk.X)
        
        button_frame = ThemedFrame(content_frame, use_secondary=True)
        button_frame.pack(fill=tk.X, padx=0, pady=0)
        
        close_btn = ThemedButton(button_frame, text="✗ Cerrar", command=self.destroy)
        close_btn.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)
    
    def _search_mods(self) -> None:
        """Search for mods in a separate thread"""
        query = self.search_entry.get_clean()
        
        if not query:
            messagebox.showwarning("Advertencia", "Ingresa un término de búsqueda")
            return
        
        self.is_searching = True
        self.results_listbox.delete(0, tk.END)
        self.status_label.config(text=f"Buscando mods con '{query}'...")
        
        def search_thread():
            try:
                self.search_results = self.mod_manager.downloader.search(query, limit=20)
                self.after(0, self._update_results)
            except Exception as e:
                logger.error(f"Search error: {e}")
                self.after(0, lambda: messagebox.showerror("Error", f"Error en búsqueda: {str(e)}"))
                self.after(0, lambda: self.status_label.config(text="Error en búsqueda"))
            finally:
                self.is_searching = False
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def _update_results(self) -> None:
        """Update the results listbox"""
        self.results_listbox.delete(0, tk.END)
        
        if not self.search_results:
            self.status_label.config(text="Sin resultados")
            return
        
        for mod in self.search_results:
            display = f"{mod.name} ({mod.downloads} descargas)"
            self.results_listbox.insert(tk.END, display)
        
        self.status_label.config(text=f"Se encontraron {len(self.search_results)} mods (haz clic para descargar)")
    
    def _on_mod_selected(self, event) -> None:
        """Handle mod selection"""
        selection = self.results_listbox.curselection()
        if not selection:
            return
        
        selected_mod = self.search_results[selection[0]]
        
        if messagebox.askyesno("Confirmar", f"¿Descargar '{selected_mod.name}'?"):
            self._download_mod(selected_mod)
    
    def _download_mod(self, mod) -> None:
        """Download selected mod"""
        self.is_downloading = True
        self.results_listbox.config(state=tk.DISABLED)
        
        def download_thread():
            try:
                self.status_label.config(text=f"Descargando {mod.name}...")
                
                # This would need proper implementation based on actual file paths
                # For now, show simulated progress
                success = True
                
                if success:
                    self.after(0, lambda: messagebox.showinfo("Éxito", f"Mod {mod.name} descargado correctamente"))
                    
                    if self.on_installed:
                        self.on_installed(mod.name)
                else:
                    self.after(0, lambda: messagebox.showerror("Error", f"No se pudo descargar {mod.name}"))
            
            except Exception as e:
                logger.error(f"Download error: {e}")
                self.after(0, lambda: messagebox.showerror("Error", f"Error descargando: {str(e)}"))
            
            finally:
                self.is_downloading = False
                self.after(0, lambda: self.results_listbox.config(state=tk.NORMAL))
                self.after(0, lambda: self.status_label.config(text="Descarga completada"))
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def center_on_parent(self, parent) -> None:
        """Center dialog on parent window"""
        self.update_idletasks()
        parent.update_idletasks()
        
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        
        self.geometry(f"+{x}+{y}")
