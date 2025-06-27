# main.py
import tkinter as tk
from Login_ui_demo import LoginScreen
from Dash_ui_demo import DashboardScreen


class MainApplication:
    def __init__(self, master):
        # "master" es la ventana principal (el objeto tk.Tk()).
        # La guardamos en self.master para poder usarla en toda la clase.
        self.master = master

        # ---- Configuración de la Ventana Principal ----
        master.title("Detector de Ratas_v0")
        master.configure(bg="#0c0c2b")
        master.state('zoomed')  # Maximiza la ventana al iniciar.

        # ---- Creación del "Escenario" ----
        # Creamos un Frame que actuará como un "escenario" o contenedor.
        # En lugar de poner las pantallas directamente en la ventana, las pondremos
        # en este contenedor. Esto evita que se mezclen con otros posibles widgets.
        self.container = tk.Frame(master)
        self.container.pack(fill="both", expand=True)  # Ocupa todo el espacio disponible.

        # ---- Creación de las Pantallas (Frames) ----
        # Creamos instancias de nuestras pantallas, pero AÚN NO las mostramos.
        # Son como actores esperando su turno para salir a escena.
        #
        # A cada pantalla le pasamos una "receta" (un callback) para que sepa
        # qué hacer cuando ocurra algo importante.
        self.login_screen = LoginScreen(self.container, on_login_success=self.show_dashboard)
        # ^ Le decimos a LoginScreen: "Cuando el login sea exitoso, ejecuta la función 'show_dashboard'".

        self.dashboard_screen = DashboardScreen(self.container, on_logout_callback=self.show_login)
        # ^ Le decimos a DashboardScreen: "Cuando se cierre sesión, ejecuta la función 'show_login'".

        # ---- Controlador de la Pantalla Actual ----
        # Esta variable nos ayudará a saber qué pantalla está visible en cada momento.
        # Inicia vacía porque al principio no hay ninguna.
        self.current_frame = None

        # ---- Punto de Inicio ----
        # Llamamos a esta función para mostrar la primera pantalla de nuestra aplicación.
        self.show_login()

    def show_login(self):
        """Oculta la pantalla actual (si hay una) y muestra la pantalla de login."""
        print("Mostrando pantalla de Login...")

        # Si ya hay una pantalla en el "escenario" (current_frame no es None)...
        if self.current_frame:
            self.current_frame.pack_forget()  # ...la quitamos del escenario.

        # Ponemos la pantalla de login en el escenario.
        self.login_screen.pack(fill="both", expand=True)

        # Y ahora recordamos que la pantalla de login es la que está visible.
        self.current_frame = self.login_screen

    def show_dashboard(self):
        """Oculta la pantalla actual y muestra el dashboard."""
        print("Mostrando Dashboard...")

        # Si ya hay una pantalla en el "escenario"...
        if self.current_frame:
            self.current_frame.pack_forget()  # ...la quitamos.

        # Ponemos el dashboard en el escenario.
        self.dashboard_screen.pack(fill="both", expand=True)

        # Y recordamos que el dashboard es ahora la pantalla visible.
        self.current_frame = self.dashboard_screen


# --------------- Punto de Entrada de la Aplicación ---------------
if __name__ == "__main__":
    # 1. Creamos la ÚNICA ventana principal de toda la aplicación.
    root = tk.Tk()

    # 2. Creamos una instancia de nuestra clase controladora (el "cerebro").
    app = MainApplication(root)

    # 3. Iniciamos el bucle de eventos, que mantiene la ventana abierta.
    root.mainloop()