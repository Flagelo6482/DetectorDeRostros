import tkinter as tk
from login_dash import LoginScreen
from detector_dash import DetectScreen
from guardar_dash import SaveScreen


class MainApplication:
    def __init__(self, master, funciones, recursos):
        self.master = master  # Ventana de tkinter
        self.funciones = funciones  # Diccionari de las funciones que tenemos
        self.recursos = recursos  # Diccionario de lo recursos que pasamos como el modelo y base de datos

        # Configuramos la interfaz con la ventana que en este caso es "master"
        # master.title("Detector de Rostros v1.0")
        master.configure(bg="#0c0c2b")
        master.state('zoomed')

        # ---- Creación del "Escenario" ----
        # Un Frame contenedor para intercambiar las diferentes pantallas.
        self.container = tk.Frame(master)
        self.container.pack(fill="both", expand=True)

        # --- Registramos pantallas ---
        self._registrar_pantallas()  # <- Aquí se crean TODAS las pantallas con sus parámetros
        self.mostrar_pantalla("login")  # <- Solo se activa la pantalla de login

    # --- Funcion para registrar las pantallas ---
    def _registrar_pantallas(self):
        """Registra todas las pantallas disponibles."""
        self.pantallas = {
            "login": LoginScreen(
                self.container,
                self.funciones,
                self.recursos,
                self.mostrar_pantalla,  # << Único callback necesario
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

    # --- FUNCION PARA MOSTRAR LA PRIMERA PANTALLA QUE ES "Login ---
    def mostrar_pantalla(self, nombre_pantalla):
        """Muestra la pantalla especificada y oculta la actual."""
        if hasattr(self, 'pantalla_actual'):
            self.pantalla_actual.pack_forget()

        self.pantalla_actual = self.pantallas[nombre_pantalla]
        self.pantalla_actual.pack(fill="both", expand=True)