import os
import tkinter as tk
from tkinter import Toplevel, messagebox
from funciones import MINECRAFT_DIR

def abrir_gestor_mods(parent, version_actual):
    win = Toplevel(parent)
    win.title("Gestor de Mods")
    win.geometry("600x500")
    win.configure(bg="#2c3e50")

    mods_folder = os.path.join(MINECRAFT_DIR, "mods")

    # Lista de mods
    frame_lista = tk.Frame(win, bg="#2c3e50")
    frame_lista.pack(fill='both', expand=True, padx=10, pady=10)

    tk.Label(
        frame_lista,
        text="Mods instalados:",
        bg="#2c3e50",
        fg="white",
        font=("Arial", 12, "bold")
    ).pack(anchor='w')

    mods_listbox = tk.Listbox(
        frame_lista,
        bg="#34495e",
        fg="white",
        width=50,
        height=15
    )
    mods_listbox.pack(side='left', fill='both', expand=True)

    scroll = tk.Scrollbar(frame_lista, command=mods_listbox.yview)
    scroll.pack(side='right', fill='y')
    mods_listbox.config(yscrollcommand=scroll.set)

    def cargar_mods():
        mods_listbox.delete(0, tk.END)
        if not os.path.exists(mods_folder):
            os.makedirs(mods_folder)
        for f in os.listdir(mods_folder):
            if f.endswith(".jar"):
                mods_listbox.insert(tk.END, f)

    cargar_mods()

    # Buscar mod
    frame_buscar = tk.Frame(win, bg="#2c3e50")
    frame_buscar.pack(fill='x', padx=10, pady=10)

    tk.Label(
        frame_buscar,
        text="Buscar mod en Modrinth:",
        bg="#2c3e50",
        fg="white"
    ).grid(row=0, column=0, sticky='w')

    entry_buscar = tk.Entry(frame_buscar, width=40)
    entry_buscar.grid(row=1, column=0, padx=5, pady=5)

    estado = tk.Label(frame_buscar, text="", bg="#2c3e50", fg="white")
    estado.grid(row=2, column=0, sticky='w')

    def buscar_mod():
        nombre = entry_buscar.get().strip()
        if not nombre:
            estado.config(text="Ingresa un nombre", fg="yellow")
            return

        estado.config(text="Buscando...")
        win.update()

        try:
            from funciones import buscar_mod, instalar_mod_con_dependencias
            resultados = buscar_mod(nombre)

            if not resultados:
                estado.config(text="No se encontro ningun mod", fg="red")
                return

            mod = resultados[0]
            instalar_mod_con_dependencias(mod["id"], version_actual)

            estado.config(text="Instalado correctamente", fg="#2ecc71")
            cargar_mods()

        except Exception as e:
            estado.config(text=str(e), fg="red")

    tk.Button(
        frame_buscar,
        text="Buscar e instalar",
        command=buscar_mod,
        bg="#3498db",
        fg="white"
    ).grid(row=1, column=1, padx=10)

    # Eliminar mod
    def eliminar_mod():
        sel = mods_listbox.curselection()
        if not sel:
            messagebox.showwarning("Error", "Selecciona un mod")
            return

        mod = mods_listbox.get(sel[0])
        ruta = os.path.join(mods_folder, mod)
        os.remove(ruta)
        cargar_mods()
        messagebox.showinfo("Eliminado", f"{mod} fue eliminado")

    tk.Button(
        win,
        text="Eliminar Mod Seleccionado",
        command=eliminar_mod,
        bg="#e74c3c",
        fg="white"
    ).pack(pady=10)






