# Interfaz_UI/login_ui.py

import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self, master, on_login_success_callback, on_close_callback):
        self.master = master
        self.on_login_success_callback = on_login_success_callback # Callback para cambiar de pantalla
        self.on_close_callback = on_close_callback # Callback para cerrar la aplicación

        self.frame = tk.Frame(master, bg="#0c0c2b", padx=20, pady=20) # Un frame para contener los widgets

        tk.Label(self.frame, text="Pantalla de Inicio de Sesión", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.frame, text="Usuario:").pack()
        self.user_entry = tk.Entry(self.frame)
        self.user_entry.pack()

        tk.Label(self.frame, text="Contraseña:").pack()
        self.pass_entry = tk.Entry(self.frame, show="*")
        self.pass_entry.pack()

        tk.Button(self.frame, text="Login (Dummy)", command=self._mock_login).pack(pady=10)
        # Añadir un botón para cerrar la aplicación
        tk.Button(self.frame, text="Cerrar", command=self.on_close_callback).pack(pady=5)

    def _mock_login(self):
        """Simula un intento de login y llama al callback si es 'exitoso'."""
        if self.user_entry.get() == "test" and self.pass_entry.get() == "123":
            messagebox.showinfo("Login", "Login simulado exitoso!")
            self.on_login_success_callback() # Llama al método show_dashboard de MainApplication
        else:
            messagebox.showerror("Login", "Credenciales incorrectas (simuladas).")


    def show(self):
        """Muestra esta pantalla."""
        self.frame.pack(expand=True, fill="both") # Empaqueta el frame para que sea visible

    def hide(self):
        """Oculta esta pantalla."""
        self.frame.pack_forget() # Desempaqueta el frame para que no sea visible
