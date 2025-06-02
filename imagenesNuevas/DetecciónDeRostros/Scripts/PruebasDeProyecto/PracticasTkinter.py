import tkinter as tk
from tkinter import font, messagebox    #messagebox es para mostrar alertas alertantes


# --------------- Función para verificar el login ---------------
def verificar_login(username, password, login, main_label):
    """
    Verificamos las credenciales ingresadas por el usuario
    :param username: Nombre de usuario
    :param password: Contraseña del usuario
    :param login:
    :param main_label: enviamos un label con contenido
    :return: Retorna un TRUE o FALSE dependiendo si fue exitoso el inicio de sesión
    """
    usuario = username.get()
    contrasena = password.get()

    #Generamos unas credenciales de prueba(luego se guardara en una base de datos)
    if usuario == "frank" and contrasena == "JCVH454":
        messagebox.showinfo("Autenticación exitosa", "¡Bienvenido al Detector de Ratas!")
        #Si nos autenticamos correctamente, destruimos el frame del login
        login.destroy()
        #Luego mostramos el contenido principal de la aplicación
        mostrar_contenido_principal(main_label)
    else:
        messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos.")
        #Limpiamos los datos de los campos de entrada
        password.delete(0, tk.END)

# --------------- Función para mostrar el contenido ---------------
def mostrar_contenido_principal(main_label):
    """
    Mostramos el contenido privado de la aplicación luego de autenticarnos correctamente
    :param main_label: Enviamos un label con contenido para mostrar
    :return:
    """
    main_label.pack(fill="x", pady=100)  #Mostramos y empaquetamos el label en la ventana

# --------------- Creamos la interfaz del login ---------------
def crear_interfaz_login(ventana, main_label):
    """
    Crea y muestra la interfaz para el login
    :param ventana: La ventana principal de Tkinter
    :param main_label: El label principal de bienvenida que se pasará a verificar_login
    :return: El frame del login
    """
    #Creamos un frame(caja) para agrupar los elementos del login
    login_frame = tk.Frame(ventana, bg="#0c0c2b")
    login_frame.pack(expand=True)   #Hace que el frame ocupe el centro de la ventana

    #Titulo del login
    login_title = tk.Label(
        login_frame,
        text="Iniciar sesión",
        font=("Verdana", 40, "bold"),
        bg="#0c0c2b",
        fg="#a8dadc"
    )
    login_title.pack(pady=30)

    #Campo del usuario
    username_label = tk.Label(
        login_frame,
        text="Usuario:",
        font=("Verdana", 16),
        bg="#0c0c2b",
        fg="#a8dadc"
    )
    username_label.pack(pady=5)

    username_entry = tk.Entry(
        login_frame,
        font=("Verdana", 14),
        width=30,
        bg="#1a1a4a",  # Fondo más oscuro para el campo
        fg="#a8dadc",  # Texto claro
        insertbackground="#a8dadc"  # Color del cursor
    )
    username_entry.pack(pady=5)
    username_entry.focus_set()  #Pone el cursor en este campo al iniciar :D

    #Campo de contraseña
    password_label = tk.Label(
        login_frame,
        text="Contraseña:",
        font=("Verdana", 16),
        bg="#0c0c2b",
        fg="#a8dadc"
    )
    password_label.pack(pady=5)

    password_entry = tk.Entry(
        login_frame,
        font=("Verdana", 14),
        width=30,
        show="*",  # Esto oculta la contraseña con asteriscos
        bg="#1a1a4a",
        fg="#a8dadc",
        insertbackground="#a8dadc"
    )
    password_entry.pack(pady=5)

    #Boton de para INICIAR SESIÓN
    login_boton = tk.Button(
        login_frame,
        text="Ingresar",
        font=("Verdana", 18, "bold"),
        bg="#4CAF50",  # Un verde para el botón de login
        fg="white",
        activebackground="#45a049",
        activeforeground="white",
        relief="flat",  # Estilo plano,
        command=lambda: verificar_login(username_entry, password_entry, login_frame, main_label)
    )
    login_boton.pack(pady=20)

    #Permite presionar Enter para iniciar sesión
    ventana.bind('<Return>', lambda event: verificar_login(username_entry, password_entry, login_frame, main_label))

    return login_frame  #Retornamos el frame de login para destruirlo :c

# --------------- Función para la creación de la ventana ---------------
def iniciar_ventana():
    # Ventana grafica
    ventana = tk.Tk()
    ventana.title("Detector de Ratas_v0")
    ventana.configure(bg="#0c0c2b")
    ventana.state('zoomed')  # Solo funciona en windows papa
    return ventana  #Retornamos la ventana para usarla cuando la llamemos

# --------------- Lógica de la app ---------------

#1.Creamos una ventana con la función que crea la ventana pechonalizada
ventana = iniciar_ventana()

#2.Creamos el label de Bienvenida pero NO lo agregamos a la ventana hasta iniciar sesión
#Solo lo guardamos en una variable para usarlo despues de el inicio de sesión
welcome_label = tk.Label(
    ventana,
    text="Bienvenido",
    font=("Verdana", 70, "bold"),
    bg="#0c0c2b",
    fg="#a8dadc"
)

#3.Creamos la interfaz del login con nuestra función, pasamos el label principal para que el login lo muestre
login_screen_frame = crear_interfaz_login(ventana, welcome_label)

ventana.mainloop()
# # Esto evita que se ejecute automáticamente al importar desde otro archivo
# if __name__ == "__main__":
#     iniciar_ventana()