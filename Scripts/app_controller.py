import tkinter as tk
from login_dash import LoginScreen
from detector_dash import DetectScreen
from guardar_dash import SaveScreen


class MainApplication:
    def __init__(self, master, funciones, recursos):
        self.master = master
        self.funciones = funciones
        self.recursos = recursos

        master.configure(bg="#0c0c2b")
        master.state('zoomed')

        self.container = tk.Frame(master)
        self.container.pack(fill="both", expand=True)

        self._registrar_pantallas()
        self.mostrar_pantalla("login")

    def _registrar_pantallas(self):
        """Registra todas las pantallas disponibles."""
        self.pantallas = {
            "login": LoginScreen(
                self.container,
                self.funciones,
                self.recursos,
                self.mostrar_pantalla,
                self.master
            ),
            "detectar": DetectScreen(
                self.container,
                self.funciones,
                self.recursos,
                self.mostrar_pantalla,
                self.master
            ),
            "guardar": SaveScreen(
                self.container,
                self.funciones,
                self.recursos,
                self.mostrar_pantalla,
                self.master
            )
        }

    def mostrar_pantalla(self, nombre_pantalla):
        """Muestra la pantalla especificada y oculta la actual."""
        if hasattr(self, 'pantalla_actual'):
            self.pantalla_actual.pack_forget()

        self.pantalla_actual = self.pantallas[nombre_pantalla]
        self.pantalla_actual.pack(fill="both", expand=True)

        if hasattr(self.pantalla_actual, 'display_title'):
            self.master.title(self.pantalla_actual.display_title)
        else:
            self.master.title("Aplicación de Detección")
