import tkinter as tk
from tkinter import ttk, StringVar, messagebox
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Window.Componentes import PlaceholderEntry, PlayButton
from Window.GestorMods import abrir_gestor_mods
from Window.VentanaInstalar import abrir_ventana_instalacion
from .Perfiles import ui_mostrar_nuevo_perfil, ui_guardar_perfil, ui_eliminar_perfil
from Window.Utilidades import estilos_botones

from funciones import obtener_versiones_instaladas, ejecutar_minecraft, MINECRAFT_DIR
import perfiles
import os

def lanzar_launcher():
    ventana = tk.Tk()
    ventana.title("OpenLauncherProyect")
    ventana.geometry("1000x800")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    perfiles.inicializar_perfiles()
    perfil_actual = StringVar(value="default")

    # Cabecera
    frame_cab = tk.Frame(ventana, bg="#34495e")
    frame_cab.pack(fill='x', pady=10)
    tk.Label(frame_cab, text="Open Launcher Proyect",
             font=('Arial', 14, 'bold'), bg="#34495e", fg="white").pack()

    # Cuerpo
    frame_principal = tk.Frame(ventana, bg="#2c3e50")
    frame_principal.pack(fill='both', expand=True)

    # Panel izquierdo
    frame_controls = tk.Frame(frame_principal, bg="#2c3e50")
    frame_controls.grid(row=0, column=0, padx=20, pady=10)

    # Perfiles
    frame_perfiles = tk.Frame(frame_controls, bg="#2c3e50")
    frame_perfiles.pack(fill='x')

    tk.Label(frame_perfiles, text="Perfil:", bg="#2c3e50", fg="white").pack(side='left')
    lista = perfiles.listar_perfiles()
    perfil_menu = ttk.Combobox(frame_perfiles, textvariable=perfil_actual,
                               values=lista, state="readonly")
    perfil_menu.pack(side='left', fill='x', expand=True)

    # Campos
    entry_nombre = PlaceholderEntry(frame_controls, placeholder="Nombre de Minecraft")
    entry_nombre.pack(pady=10)

    entry_ram = PlaceholderEntry(frame_controls, placeholder="RAM (GB)")
    entry_ram.pack(pady=10)

    # Versiones
    versiones = obtener_versiones_instaladas()
    vers_var = StringVar(value=versiones[0] if versiones else "")

    def actualizar_versiones():
        nuevas = obtener_versiones_instaladas()
        menu = versiones_menu["menu"]
        menu.delete(0, "end")
        for v in nuevas:
            menu.add_command(label=v, command=lambda x=v: vers_var.set(x))
        if nuevas:
            vers_var.set(nuevas[0])

    versiones_menu = tk.OptionMenu(frame_controls, vers_var, *versiones)
    versiones_menu.config(bg="#3498db", fg="white")
    versiones_menu.pack(pady=10)

    # Botones de perfiles
    tk.Button(frame_perfiles, text="+", command=lambda: 
              ui_mostrar_nuevo_perfil(ventana, entry_nombre, entry_ram, perfil_menu, perfil_actual), **estilos_botones).pack(side='left')

    tk.Button(frame_perfiles, text="Guardar", command=lambda:
              ui_guardar_perfil(perfil_actual, entry_nombre, entry_ram), **estilos_botones).pack(side='left')

    tk.Button(frame_perfiles, text="X", command=lambda:
              ui_eliminar_perfil(ventana, perfil_menu, perfil_actual), **estilos_botones).pack(side='left')

    # Gestor de mods
    tk.Button(frame_controls, text="Gestor de Mods",
              command=lambda: abrir_gestor_mods(ventana, vers_var.get()),
              **estilos_botones).pack(pady=10)

    # Instalar versiones
    tk.Button(frame_controls, text="Instalar Versiones",
              command=lambda: abrir_ventana_instalacion(ventana, actualizar_versiones),
              **estilos_botones).pack(pady=10)

    # Boton Jugar
    def ejecutar():
        perfiles.actualizar_perfil(
            perfil_actual.get(),
            entry_nombre.get_clean(),
            entry_ram.get_clean()
        )
        ejecutar_minecraft(entry_nombre.get_clean(), vers_var.get(), entry_ram.get_clean(), ventana.destroy)

    PlayButton(frame_controls, command=ejecutar).pack(pady=20)

    ventana.mainloop()




