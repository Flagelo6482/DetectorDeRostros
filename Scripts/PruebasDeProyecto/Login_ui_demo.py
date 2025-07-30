# login_ui.py
import tkinter as tk
from tkinter import messagebox


class LoginScreen(tk.Frame):
    def __init__(self, master, on_login_success):
        """
        Recibe el 'master' (ventana principal) y un callback
        para notificar cuando el login sea exitoso.
        """
        super().__init__(master, bg="#0c0c2b")
        self.on_login_success = on_login_success

        # Creamos la UI dentro de 'self' (el Frame)
        login_title = tk.Label(self, text="Iniciar sesión", font=("Verdana", 40, "bold"), bg="#0c0c2b", fg="#a8dadc")
        login_title.pack(pady=30)

        username_label = tk.Label(self, text="Usuario:", font=("Verdana", 16), bg="#0c0c2b", fg="#a8dadc")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Verdana", 14), width=30, bg="#1a1a4a", fg="#a8dadc",
                                       insertbackground="#a8dadc")
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        password_label = tk.Label(self, text="Contraseña:", font=("Verdana", 16), bg="#0c0c2b", fg="#a8dadc")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Verdana", 14), width=30, show="*", bg="#1a1a4a", fg="#a8dadc",
                                       insertbackground="#a8dadc")
        self.password_entry.pack(pady=5)

        login_boton = tk.Button(self, text="Ingresar", font=("Verdana", 18, "bold"), bg="#4CAF50", fg="white",
                                command=self._verify_login)
        login_boton.pack(pady=20)

        # Hacemos que la tecla Enter también funcione
        master.bind('<Return>', self._verify_login_event)

    def _verify_login_event(self, event):
        # Wrapper para manejar el argumento 'event' de bind
        self._verify_login()

    def _verify_login(self):
        """
        Verifica las credenciales y llama al callback si son correctas.
        """
        usuario = self.username_entry.get()
        contrasena = self.password_entry.get()

        if usuario == "1" and contrasena == "1":
            messagebox.showinfo("Autenticación exitosa", "¡Bienvenido!")
            # Notificamos al script principal que el login fue exitoso
            self.on_login_success()
        else:
            messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, tk.END)
