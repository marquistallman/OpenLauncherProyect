"""Reusable UI components"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from ..utils.config import Config


class PlaceholderEntry(tk.Entry):
    """Entry widget with placeholder text"""
    
    def __init__(
        self,
        master=None,
        placeholder: str = "",
        placeholder_color: str = Config.COLORS['grey'],
        **kwargs
    ):
        kwargs.setdefault('bg', Config.COLORS['surface'])
        kwargs.setdefault('fg', Config.COLORS['primary'])
        kwargs.setdefault('font', ('Segoe UI', 10))
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('borderwidth', 1)
        kwargs.setdefault('highlightthickness', 1)
        kwargs.setdefault('highlightcolor', Config.COLORS['accent'])
        kwargs.setdefault('highlightbackground', Config.COLORS['border'])
        
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg = Config.COLORS['primary']
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._show_placeholder()
    
    def _show_placeholder(self) -> None:
        """Display placeholder text"""
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
    
    def _on_focus_in(self, event) -> None:
        """Handle focus in event"""
        if self.cget('fg') == self.placeholder_color:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg)
    
    def _on_focus_out(self, event) -> None:
        """Handle focus out event"""
        if not self.get():
            self._show_placeholder()
    
    def get_clean(self) -> str:
        """Get text value, excluding placeholder"""
        is_placeholder = self.cget('fg') == self.placeholder_color
        return "" if is_placeholder else self.get()
    
    def set_text(self, text: str) -> None:
        """Set text value"""
        self.delete(0, tk.END)
        if text:
            self.insert(0, text)
            self.config(fg=self.default_fg)
        else:
            self._show_placeholder()
    
    def clear(self) -> None:
        """Clear the entry"""
        self.delete(0, tk.END)
        self._show_placeholder()


class PlayButton(tk.Button):
    """Custom play button widget with play icon"""
    
    def __init__(self, master=None, command: Optional[Callable] = None, **kwargs):
        # Set default styling for a prominent play button
        kwargs.setdefault('bg', Config.COLORS['success'])
        kwargs.setdefault('fg', Config.COLORS['white'])
        kwargs.setdefault('font', ('Segoe UI', 16, 'bold'))
        kwargs.setdefault('padx', 50)
        kwargs.setdefault('pady', 18)
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('activebackground', Config.COLORS['success_hover'])
        kwargs.setdefault('activeforeground', Config.COLORS['white'])
        kwargs.setdefault('bd', 0)
        
        super().__init__(
            master,
            text="▶ JUGAR",
            command=command,
            **kwargs
        )
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def _on_hover(self, event):
        """Handle hover effect"""
        self.config(bg=Config.COLORS['success_hover'])
    
    def _on_leave(self, event):
        """Remove hover effect"""
        self.config(bg=Config.COLORS['success'])
    
    def highlight(self) -> None:
        """Highlight the button"""
        self.config(bg=Config.COLORS['success_hover'])
    
    def unhighlight(self) -> None:
        """Remove highlight from button"""
        self.config(bg=Config.COLORS['success'])


class ThemedFrame(tk.Frame):
    """Frame with theme colors"""
    
    def __init__(self, master=None, use_secondary: bool = False, **kwargs):
        if use_secondary:
            bg_color = Config.COLORS['secondary']
        else:
            bg_color = Config.COLORS['primary']
        super().__init__(master, bg=bg_color, **kwargs)


class ThemedLabel(tk.Label):
    """Label with theme colors"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['primary'])
        kwargs.setdefault('fg', Config.COLORS['white'])
        kwargs.setdefault('font', ('Segoe UI', 10))
        super().__init__(master, **kwargs)


class ThemedButton(tk.Button):
    """Button with theme styling"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['accent'])
        kwargs.setdefault('fg', Config.COLORS['white'])
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('padx', 18)
        kwargs.setdefault('pady', 10)
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('font', ('Segoe UI', 10))
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('activebackground', Config.COLORS['accent_light'])
        kwargs.setdefault('activeforeground', Config.COLORS['white'])
        
        super().__init__(master, **kwargs)
        self.default_bg = self['bg']
        self.hover_bg = Config.COLORS['accent_light']
        
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def _on_hover(self, event):
        """Handle hover effect"""
        self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        """Remove hover effect"""
        self.config(bg=self.default_bg)


class ScrollableFrame(tk.Frame):
    """Frame with scrollbar support"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['primary'])
        super().__init__(master, **kwargs)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(
            self, 
            bg=Config.COLORS['primary'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg=Config.COLORS['primary'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Register frame in canvas
        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event) -> None:
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def get_frame(self) -> tk.Frame:
        """Get the scrollable frame for adding widgets"""
        return self.scrollable_frame


class StatusBar(tk.Frame):
    """Status bar for displaying messages"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['secondary'])
        super().__init__(master, **kwargs)
        
        self.status_label = tk.Label(
            self,
            text="Ready",
            justify=tk.LEFT,
            bg=Config.COLORS['secondary'],
            fg=Config.COLORS['white'],
            font=('Segoe UI', 10),
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10, fill=tk.X, expand=True)
    
    def set_status(self, message: str, status_type: str = "info") -> None:
        """Update status message"""
        color_map = {
            'info': Config.COLORS['white'],
            'success': Config.COLORS['success'],
            'error': Config.COLORS['danger'],
            'warning': Config.COLORS['warning']
        }
        
        self.status_label.config(
            text=message,
            fg=color_map.get(status_type, Config.COLORS['white'])
        )
    
    def clear_status(self) -> None:
        """Clear status message"""
        self.set_status("Ready")
