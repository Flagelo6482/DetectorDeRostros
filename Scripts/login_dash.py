import tkinter as tk
from tkinter import messagebox


class LoginScreen(tk.Frame):
    def __init__(self, master, funciones, recursos, controlador, root_window):
        super().__init__(master)  # Inicializa tk.Frame
        self.root_window = root_window
        self.display_title = "Inicio de Sesión"
        self.controlador = controlador
        self.funciones = funciones  # Diccionario de las funciones que tenemos
        self.recursos = recursos  # Diccionario de los recursos que pasamos como el modelo y base de datos

        self.config(bg="#0c0c2b")
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los elementos de la interfaz"""
        # TITULO
        login_title = tk.Label(self, text="Iniciar sesión", font=("Verdana", 40, "bold"), bg="#0c0c2b", fg="#a8dadc")
        login_title.pack(pady=30)

        # Campos de entrada
        tk.Label(self, text="Usuario:", font=("Verdana", 16), bg="#0c0c2b", fg="#a8dadc").pack(pady=5)
        self.entry_usuario = tk.Entry(self, font=("Verdana", 14), width=30, bg="#1a1a4a", fg="#a8dadc",
                                       insertbackground="#a8dadc")
        self.entry_usuario.pack(pady=5)

        tk.Label(self, text="Contraseña:", font=("Verdana", 16), bg="#0c0c2b", fg="#a8dadc").pack(pady=5)
        self.entry_password = tk.Entry(self, font=("Verdana", 14), width=30, show="*", bg="#1a1a4a", fg="#a8dadc",
                                       insertbackground="#a8dadc")
        self.entry_password.pack(pady=5)

        # Botón de login - Ahora valida ANTES de llamar al callback
        tk.Button(
            self,
            text="Iniciar sesión",
            font=("Verdana", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self._validar_login  # <<-- Primero valida, luego usa el callback
        ).pack(pady=20)

        # Botón para cerrar
        # tk.Button(
        #     self,
        #     text="Cerrar"
        # ).pack()

        # Botón para cerrar el programa
        tk.Button(
            self,
            text="Cerrar el programa",
            command=self.master.quit  # Cierra la aplicación
        ).pack(pady=20)

    def _validar_login(self):
        """Valida credenciales y llama al callback si son correctas"""
        if self._credenciales_validas():  # Si la validación es exitosa
            self.controlador("detectar")  # <<-- Ejecuta el callback para cambiar de pantalla
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def _credenciales_validas(self):
        """Lógica de validación (personaliza esto)"""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        return usuario == "admin" and password == "123"