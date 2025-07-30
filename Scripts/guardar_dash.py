import tkinter as tk

class SaveScreen(tk.Frame):
    def __init__(self, master, funciones, recursos, controlador, root_window):
        super().__init__(master)  # Inicializa tk.Frame
        self.root_window = root_window
        self.root_window.title("Guardar datitos")
        self.controlador = controlador
        self.funciones = funciones  # Diccionario de las funciones que tenemos
        self.recursos = recursos

        self.config(bg="#0c0c2b")
        self._crear_widgets()

    def _crear_widgets(self):
        """ACA AGREGAMOS LOS OBJETOS DE LA INTERFAZ QUE YA CREAMOS(BUSCAR)"""

        tk.Button(
            self,
            text="Ir a detectar rostros",
            command=self._pantalla_detector_rostros
        ).pack(pady=10)

        # Botón para cerrar el programa
        tk.Button(
            self,
            text="Cerrar el programa",
            command=self.master.quit  # Cierra la aplicación
        ).pack(pady=20)

    def _pantalla_detector_rostros(self):
        """Nos vamos a la pantalla de detección de rostros"""
        self.controlador("detectar")