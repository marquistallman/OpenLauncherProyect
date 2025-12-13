import tkinter as tk
from tkinter import Toplevel, messagebox
from funciones import instalar_version, instalar_forge, instalar_fabric

def abrir_ventana_instalacion(parent, actualizar_versiones):
    ventana = Toplevel(parent)
    ventana.title("Instalar version")
    ventana.geometry("300x250")
    ventana.configure(bg="#2c3e50")

    tk.Label(ventana, text="Version:", bg="#2c3e50", fg="white").pack(pady=5)
    entry_version = tk.Entry(ventana)
    entry_version.pack(pady=5)

    tipo = tk.StringVar(value="vanilla")

    for t in ["vanilla", "forge", "fabric"]:
        tk.Radiobutton(
            ventana,
            text=t.capitalize(),
            value=t,
            variable=tipo,
            bg="#2c3e50",
            fg="white",
            selectcolor="#34495e"
        ).pack()

    label_estado = tk.Label(ventana, text="", bg="#2c3e50", fg="white")
    label_estado.pack(pady=5)

    def instalar():
        version = entry_version.get().strip()
        if not version:
            messagebox.showwarning("Error", "Ingresa una Version")
            return

        label_estado.config(text="Descargando...")
        ventana.update()

        try:
            if tipo.get() == "vanilla":
                instalar_version(version)
            elif tipo.get() == "forge":
                instalar_forge(version)
            else:
                instalar_fabric(version)

            label_estado.config(text="Listo!")
            actualizar_versiones()
            ventana.after(1500, ventana.destroy)

        except Exception as e:
            label_estado.config(text="Error")
            messagebox.showerror("Error", str(e))

    tk.Button(ventana, text="Instalar", command=instalar).pack(pady=10)


