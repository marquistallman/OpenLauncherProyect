import tkinter as tk
from tkinter import Toplevel, messagebox
import perfiles

def ui_mostrar_nuevo_perfil(parent, entry_nombre, entry_ram, perfil_menu, perfil_actual):
    ventana = Toplevel(parent)
    ventana.title("Nuevo Perfil")
    ventana.geometry("300x100")
    ventana.configure(bg="#2c3e50")

    tk.Label(ventana, text="Nombre del perfil:", fg="white", bg="#2c3e50").pack()
    entry = tk.Entry(ventana)
    entry.pack()

    def crear():
        nombre = entry.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Debes ingresar un nombre")
            return

        ok = perfiles.crear_perfil(nombre, entry_nombre.get_clean(), entry_ram.get_clean())
        if not ok:
            messagebox.showwarning("Error", "Ese perfil ya existe")
            return

        perfil_menu["values"] = perfiles.listar_perfiles()
        perfil_actual.set(nombre)
        ventana.destroy()

    tk.Button(ventana, text="Crear", command=crear).pack(pady=5)


def ui_guardar_perfil(perfil_actual, entry_nombre, entry_ram):
    perfiles.actualizar_perfil(
        perfil_actual.get(),
        entry_nombre.get_clean(),
        entry_ram.get_clean()
    )
    messagebox.showinfo("Guardado", "Perfil actualizado")


def ui_eliminar_perfil(parent, perfil_menu, perfil_actual):
    nombre = perfil_actual.get()
    if nombre == "default":
        messagebox.showwarning("Error", "No puedes eliminar el perfil por defecto")
        return

    if messagebox.askyesno("Confirmar", f"Eliminar perfil '{nombre}'?"):
        perfiles.eliminar_perfil(nombre)
        perfil_menu["values"] = perfiles.listar_perfiles()
        perfil_actual.set("default")





