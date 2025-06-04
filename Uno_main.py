"""
Archivo principal del sistema GlobalTrade.
Permite gestionar productos, envíos, conversiones monetarias y documentación.
"""


import tkinter as tk
from src.interfaz import InterfazGlobalTrade

def main():
    root = tk.Tk()
    app = InterfazGlobalTrade(root)
    root.mainloop()

if __name__ == "__main__":
    main()
