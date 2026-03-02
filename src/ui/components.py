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
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg = self.cget('fg')
        
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


class PlayButton(tk.Canvas):
    """Custom play button widget"""
    
    def __init__(self, master=None, command: Optional[Callable] = None, **kwargs):
        super().__init__(
            master,
            width=120,
            height=40,
            bd=0,
            highlightthickness=0,
            bg=Config.COLORS['primary'],
            **kwargs
        )
        self.command = command
        
        # Draw button background
        self.bg_rect = self.create_rectangle(0, 0, 120, 40, fill=Config.COLORS['success'], outline="")
        
        # Draw play icon (triangle)
        self.create_polygon(40, 10, 40, 30, 60, 20, fill='white')
        
        # Draw text
        self.create_text(80, 20, text="PLAY", fill='white', font=('Arial', 10, 'bold'))
        
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _on_hover(self, event) -> None:
        """Handle mouse hover"""
        self.itemconfig(self.bg_rect, fill=Config.COLORS['success_hover'])
    
    def _on_leave(self, event) -> None:
        """Handle mouse leave"""
        self.itemconfig(self.bg_rect, fill=Config.COLORS['success'])
    
    def _on_click(self, event) -> None:
        """Handle button click"""
        if self.command:
            self.command()


class ThemedFrame(tk.Frame):
    """Frame with theme colors"""
    
    def __init__(self, master=None, use_secondary: bool = False, **kwargs):
        bg_color = Config.COLORS['secondary'] if use_secondary else Config.COLORS['primary']
        super().__init__(master, bg=bg_color, **kwargs)


class ThemedLabel(tk.Label):
    """Label with theme colors"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['primary'])
        kwargs.setdefault('fg', Config.COLORS['white'])
        super().__init__(master, **kwargs)


class ThemedButton(tk.Button):
    """Button with theme styling"""
    
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('bg', Config.COLORS['accent'])
        kwargs.setdefault('fg', Config.COLORS['white'])
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('padx', 20)
        kwargs.setdefault('pady', 10)
        kwargs.setdefault('cursor', 'hand2')
        super().__init__(master, **kwargs)


class ScrollableFrame(tk.Frame):
    """Frame with scrollbar support"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas)
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
        super().__init__(master, bg=Config.COLORS['secondary'], **kwargs)
        
        self.status_label = ThemedLabel(
            self,
            text="Ready",
            justify=tk.LEFT,
            bg=Config.COLORS['secondary']
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
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
