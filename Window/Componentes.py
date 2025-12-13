import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self['fg']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._restore_placeholder)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def _clear_placeholder(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg

    def _restore_placeholder(self, event):
        if not self.get():
            self.put_placeholder()

    def get_clean(self):
        return "" if self['fg'] == self.placeholder_color else self.get()

    def set_text(self, text):
        self.delete(0, tk.END)
        if text:
            self.insert(0, text)
            self['fg'] = self.default_fg
        else:
            self.put_placeholder()

class PlayButton(tk.Canvas):
    def __init__(self, master=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bd=0, highlightthickness=0, width=120, height=40)
        self.command = command

        self.bg = self.create_rectangle(0, 0, 120, 40, fill="#27ae60", outline="")
        self.create_polygon(40, 10, 40, 30, 60, 20, fill='white')
        self.create_text(80, 20, text="JUGAR", fill='white', font=('Arial', 10, 'bold'))

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        self.itemconfig(self.bg, fill="#219d54")

    def _on_leave(self, event):
        self.itemconfig(self.bg, fill="#27ae60")

    def _on_click(self, event):
        if self.command:
            self.command()





