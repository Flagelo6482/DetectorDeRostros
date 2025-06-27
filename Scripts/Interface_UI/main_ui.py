import tkinter as tk
from login_ui import LoginScreen
from dashboard_ui import DashboardScreen

# --------------- Clase para la creación de la ventana ---------------
class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Detector de Ratas_v0")
        master.configure(bg="#0c0c2b")
        master.state('zoomed')

        #1.Instanciamos las pantallas que son el inicio de sesión y dashboard
        self.login_screen = LoginScreen(master, self.show_dashboard, self.close_application)
        self.dashboard_screen = DashboardScreen(master, self.close_application)

        #2.Muestra la pantalla inicial(login)
        self.show_login()


    def show_login(self):
        """Oculta el dashboard y muestra la pantalla del login"""
        self.dashboard_screen.hide()
        self.login_screen.show()

    def show_dashboard(self):
        """Oculta el login y muestra la pantalla del dashboard"""
        self.login_screen.hide()
        self.dashboard_screen.show()

    def close_application(self):
        """Cierra la ventana principal de la app"""
        print("Cerrando app....")
        self.master.destroy()

# --------------- Código para Iniciar la Aplicación ---------------
if __name__ == "__main__":
    root = tk.Tk()              # 1. Crea la ventana raíz de la aplicación.
    app = MainApplication(root) # 2. Crea una instancia de tu clase principal, pasándole la ventana.
    root.mainloop()             # 3. Inicia el bucle de eventos, que mantiene la ventana abierta y escuchando acciones.