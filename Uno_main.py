"""
Archivo principal del sistema GlobalTrade.
Permite gestionar productos, envíos, conversiones monetarias y documentación.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os, sys

# Funciones para ejecutar los otros archivos
def ejecutar_productos():
    subprocess.run(["python", "src/Dos_productos.py"])

def ejecutar_envios():
    subprocess.run(["python", "src/Tres_envios.py"])

def ejecutar_conversion():
    subprocess.run(["python", "src/Cuatro_conversion.py"])

def ejecutar_documentacion():
    subprocess.run(["python", "src/Cinco_documentacion.py"])

def salir():
    root.destroy()


# Crear la ventana principal
root = tk.Tk()
root.title("Chronos Supply Chain - Menú Principal - GoblalTrade")
root.geometry("600x450")

# Portada
#Encabezado "Chronos Supply Chain"
titulo_frame = ttk.Frame(root)
titulo_frame.pack(pady=10)

ttk.Label(titulo_frame, text="Chronos Supply Chain", 
          font=('Arial', 16, 'bold')).pack()

logo_frame = ttk.Frame(titulo_frame)
logo_frame.pack()
ttk.Label(logo_frame, text="✈️ CHRONOS", font=('Arial', 12)).pack()
ttk.Label(logo_frame, text="Importaciones a Guatemala", font=('Arial', 10)).pack()

# Crear los botones
titulo = tk.Label(root, text="Seleccione una opción", font=("Arial", 16))
titulo.pack(pady=20)

btn_documentacion = tk.Button(root, text="Productos", command=ejecutar_productos, width=25)
btn_documentacion.pack(pady=5)

btn_envios = tk.Button(root, text="Gestión de Envíos", command=ejecutar_envios, width=25)
btn_envios.pack(pady=5)

btn_conversion = tk.Button(root, text="Conversión de Divisas", command=ejecutar_conversion, width=25)
btn_conversion.pack(pady=5)

btn_documentacion = tk.Button(root, text="Generar Documentación", command=ejecutar_documentacion, width=25)
btn_documentacion.pack(pady=5)



btn_salir = tk.Button(root, text="Salir", command=salir, width=25)
btn_salir.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
