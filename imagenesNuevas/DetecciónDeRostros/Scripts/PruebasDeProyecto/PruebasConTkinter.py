import tkinter as tk
from tkinter import filedialog, BOTTOM, CENTER, FLAT
from PIL import Image, ImageTk

#
# #Función para cargar una imagen
# def cargar_imagen():
#     ruta = filedialog.askopenfilename(  #Abrimos el explorador de archivos
#         title="Selecciona una imagen ALTOQUE",
#         filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg *.gif")]
#     )
#     if ruta:    #Si el usuario selecciona una imagen ._.
#         imagen = Image.open(ruta)
#         imagen = imagen.resize((300, 300))  #Redimensionamos en caso sea muy grande
#         image_tk = ImageTk.PhotoImage(imagen)
#         etiqueta_image.config(image=image_tk)
#         etiqueta_image.image = image_tk #Guardamos referencia para que no se borre
#
# #1.Creamos la ventana
# ventana = tk.Tk()
# ventana.title("Cargar imagen")
# ventana.geometry("1000x800")
# ventana.configure(bg="gray25")  #QUEDA EL COLOR
#
# #2.Creamos el boton para activar la función de carga de imagen
# boton = tk.Button(ventana, text="Cargue su imagen", command=cargar_imagen)
# boton.pack(pady=10)
#
# #3.Label donde se mostrara la imagen
# etiqueta_image = tk.Label(ventana)
# etiqueta_image.pack()
#
# ventana.mainloop()
# --- main.py ---
# Este es el punto de entrada de la aplicación.
# Se encarga de inicializar la ventana principal y la aplicación.

import tkinter as tk
# from tkinter import messagebox
# import ttkbootstrap as tb  # Importamos ttkbootstrap para un diseño moderno
# from ttkbootstrap.constants import *  # Importamos constantes para bootstyle
#
# # Simulamos la estructura de archivos con clases y funciones dentro de un solo script
# # En un proyecto real, estas serían importaciones de módulos separados.
#
# # --- utils/password_hasher.py ---
# # Módulo para el hashing y verificación de contraseñas usando bcrypt.
# import bcrypt
#
#
# def hash_password(password):
#     """
#     Genera un hash de la contraseña usando bcrypt.
#     El salt se genera automáticamente.
#     """
#     # Codifica la contraseña a bytes antes de hashear
#     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     # Decodifica el hash a una cadena para almacenarlo
#     return hashed.decode('utf-8')
#
#
# def verify_password(hashed_password, password):
#     """
#     Verifica si una contraseña dada coincide con un hash.
#     """
#     # Codifica el hash almacenado y la contraseña de entrada a bytes
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
#
#
# # --- database/db_manager.py ---
# # Módulo para la gestión de la base de datos SQLite.
# # Contiene funciones para crear tablas, añadir usuarios, obtener, actualizar y eliminar.
#
# import sqlite3
# import os  # Para verificar si el archivo de la base de datos existe
#
# DB_NAME = "nexus_forge.db"
#
#
# def create_db_and_tables():
#     """
#     Crea la base de datos SQLite y la tabla de usuarios si no existen.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL,
#             full_name TEXT NOT NULL,
#             email TEXT NOT NULL,
#             role TEXT NOT NULL,
#             status INTEGER DEFAULT 1, -- 1 para activo, 0 para inactivo
#             created_at TEXT DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     conn.commit()
#     conn.close()
#
#
# def add_initial_admin():
#     """
#     Añade un usuario administrador inicial si no existe ninguno con el rol 'Administrador'.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Administrador'")
#     count = cursor.fetchone()[0]
#     if count == 0:
#         # Contraseña por defecto para el admin (se recomienda cambiarla después del primer login)
#         admin_password_hash = hash_password("admin123")
#         try:
#             cursor.execute("INSERT INTO users (username, password_hash, full_name, email, role) VALUES (?, ?, ?, ?, ?)",
#                            ("admin", admin_password_hash, "Administrador Principal", "admin@empresa.com",
#                             "Administrador"))
#             conn.commit()
#             print("Administrador inicial creado: admin/admin123")
#         except sqlite3.IntegrityError:
#             # Esto no debería ocurrir si el count es 0, pero es una buena práctica
#             print("El administrador inicial ya existe (IntegrityError).")
#     conn.close()
#
#
# def get_user_by_username_and_password(username, password):
#     """
#     Busca un usuario por nombre de usuario y verifica su contraseña.
#     Retorna el diccionario del usuario si las credenciales son correctas, de lo contrario None.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#     user_data = cursor.fetchone()
#     conn.close()
#
#     if user_data:
#         # Mapeamos la tupla a un diccionario para un acceso más legible
#         user = {
#             "id": user_data[0], "username": user_data[1], "password_hash": user_data[2],
#             "full_name": user_data[3], "email": user_data[4], "role": user_data[5],
#             "status": user_data[6], "created_at": user_data[7]
#         }
#         if verify_password(user['password_hash'], password):
#             return user
#     return None
#
#
# def get_user_by_id(user_id):
#     """
#     Busca un usuario por su ID.
#     Retorna el diccionario del usuario si se encuentra, de lo contrario None.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         return {
#             "id": user_data[0], "username": user_data[1], "password_hash": user_data[2],
#             "full_name": user_data[3], "email": user_data[4], "role": user_data[5],
#             "status": user_data[6], "created_at": user_data[7]
#         }
#     return None
#
#
# def get_all_users():
#     """
#     Obtiene todos los usuarios de la base de datos.
#     Retorna una lista de diccionarios de usuarios.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users ORDER BY username")
#     rows = cursor.fetchall()
#     conn.close()
#     users = []
#     for row in rows:
#         users.append({
#             "id": row[0], "username": row[1], "password_hash": row[2],
#             "full_name": row[3], "email": row[4], "role": row[5],
#             "status": row[6], "created_at": row[7]
#         })
#     return users
#
#
# def add_user(username, password_hash, full_name, email, role, status):
#     """
#     Añade un nuevo usuario a la base de datos.
#     Retorna True si la operación fue exitosa, False si el nombre de usuario ya existe.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO users (username, password_hash, full_name, email, role, status) VALUES (?, ?, ?, ?, ?, ?)",
#             (username, password_hash, full_name, email, role, status))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         # Esto ocurre si el username ya existe debido a la restricción UNIQUE
#         return False
#     finally:
#         conn.close()
#
#
# def update_user(user_id, username, full_name, email, role, status):
#     """
#     Actualiza la información de un usuario existente.
#     Retorna True si la operación fue exitosa, False si el nombre de usuario ya existe (para otro ID).
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     try:
#         # Verificamos si el nuevo username ya existe para otro usuario
#         cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
#         if cursor.fetchone():
#             return False  # El nombre de usuario ya está en uso por otro usuario
#
#         cursor.execute("UPDATE users SET username = ?, full_name = ?, email = ?, role = ?, status = ? WHERE id = ?",
#                        (username, full_name, email, role, status, user_id))
#         conn.commit()
#         return True
#     except Exception as e:
#         print(f"Error al actualizar usuario: {e}")
#         return False
#     finally:
#         conn.close()
#
#
# def delete_user(user_id):
#     """
#     Elimina un usuario de la base de datos por su ID.
#     Retorna True si la operación fue exitosa, False en caso de error.
#     """
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
#         conn.commit()
#         return True
#     except Exception as e:
#         print(f"Error al eliminar usuario: {e}")
#         return False
#     finally:
#         conn.close()
#
#
# # --- gui/login_view.py ---
# # Vista para la pantalla de inicio de sesión.
#
# class LoginView(tb.Frame):
#     def __init__(self, master, login_callback):
#         super().__init__(master, padding=20)
#         self.login_callback = login_callback
#
#         # Configura el frame para que se expanda y ocupe todo el espacio
#         self.master.grid_columnconfigure(0, weight=1)
#         self.master.grid_rowconfigure(0, weight=1)
#         self.grid(row=0, column=0, sticky="nsew")
#
#         # Frame central para los elementos de login, para centrarlo visualmente
#         login_frame = tb.Frame(self, bootstyle="dark", padding=30, relief=FLAT)  # Usamos FLAT para un look más moderno
#         login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centra el frame en la ventana
#
#         # Título de la aplicación
#         tb.Label(login_frame, text="NexusForge", font=("Inter", 28, "bold"), bootstyle="inverse-light").pack(
#             pady=(20, 5))
#         tb.Label(login_frame, text="Sistema de Gestión de Usuarios", font=("Inter", 12),
#                  bootstyle="inverse-light").pack(pady=(0, 20))
#
#         # Campo de Usuario
#         tb.Label(login_frame, text="Usuario:", bootstyle="inverse-light", font=("Inter", 10)).pack(anchor="w", padx=10,
#                                                                                                    pady=(10, 0))
#         self.username_entry = tb.Entry(login_frame, width=40, bootstyle="dark")
#         self.username_entry.pack(pady=5, padx=10)
#         self.username_entry.bind("<Return>",
#                                  lambda event: self.password_entry.focus_set())  # Salta al siguiente campo con Enter
#
#         # Campo de Contraseña
#         tb.Label(login_frame, text="Contraseña:", bootstyle="inverse-light", font=("Inter", 10)).pack(anchor="w",
#                                                                                                       padx=10,
#                                                                                                       pady=(10, 0))
#         self.password_entry = tb.Entry(login_frame, show="*", width=40, bootstyle="dark")
#         self.password_entry.pack(pady=5, padx=10)
#         self.password_entry.bind("<Return>", lambda event: self._perform_login())  # Ejecuta login con Enter
#
#         # Botón de Acceder
#         tb.Button(login_frame, text="Acceder", command=self._perform_login, bootstyle="success", width=20).pack(pady=20)
#
#         # Mensaje de información para el usuario inicial
#         tb.Label(login_frame, text="Usuario: admin | Contraseña: admin123", font=("Inter", 9),
#                  bootstyle="inverse-light").pack(pady=5)
#
#     def _perform_login(self):
#         """
#         Intenta autenticar al usuario con las credenciales ingresadas.
#         """
#         username = self.username_entry.get()
#         password = self.password_entry.get()
#
#         user = get_user_by_username_and_password(username, password)
#
#         if user:
#             messagebox.showinfo("Éxito", f"Bienvenido, {user['full_name']}!")
#             self.login_callback(user)  # Llama al callback de éxito con el objeto usuario
#         else:
#             messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")
#
#
# # --- gui/dashboard_view.py ---
# # Vista principal del dashboard después del inicio de sesión.
# # Contiene un sidebar de navegación y un área de contenido principal.
#
# class DashboardView(tb.Frame):
#     def __init__(self, master, current_user, logout_callback):
#         super().__init__(master)
#         self.current_user = current_user
#         self.logout_callback = logout_callback
#
#         # Configura las columnas para el sidebar y el contenido principal
#         self.grid_columnconfigure(0, weight=0)  # Sidebar: ancho fijo
#         self.grid_columnconfigure(1, weight=1)  # Contenido principal: expandible
#         self.grid_rowconfigure(0, weight=1)  # Fila principal: expandible
#
#         # --- Sidebar ---
#         self.sidebar_frame = tb.Frame(self, bootstyle="primary", width=220)  # Usamos un color de acento para el sidebar
#         self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
#         self.sidebar_frame.grid_propagate(False)  # Evita que el sidebar se ajuste a su contenido
#
#         # Título del sidebar
#         tb.Label(self.sidebar_frame, text="NexusForge", font=("Inter", 18, "bold"), bootstyle="inverse-primary").pack(
#             pady=20)
#         tb.Separator(self.sidebar_frame).pack(fill="x", padx=10, pady=5)
#
#         # Información del usuario logueado
#         tb.Label(self.sidebar_frame, text=f"Usuario: {self.current_user['username']}", font=("Inter", 10),
#                  bootstyle="inverse-primary").pack(anchor="w", padx=10)
#         tb.Label(self.sidebar_frame, text=f"Rol: {self.current_user['role']}", font=("Inter", 10),
#                  bootstyle="inverse-primary").pack(anchor="w", padx=10, pady=(0, 10))
#         tb.Separator(self.sidebar_frame).pack(fill="x", padx=10, pady=5)
#
#         # Botones de navegación
#         tb.Button(self.sidebar_frame, text="Gestión de Usuarios", command=self.show_user_management,
#                   bootstyle="light-outline", cursor="hand2").pack(fill="x", padx=10, pady=5)
#         # Otros botones (deshabilitados por ahora)
#         tb.Button(self.sidebar_frame, text="Reportes (Próximamente)", bootstyle="light-outline", state="disabled",
#                   cursor="arrow").pack(fill="x", padx=10, pady=5)
#         tb.Button(self.sidebar_frame, text="Configuración (Próximamente)", bootstyle="light-outline", state="disabled",
#                   cursor="arrow").pack(fill="x", padx=10, pady=5)
#
#         tb.Separator(self.sidebar_frame).pack(fill="x", padx=10, pady=5)
#
#         # Botón de Cerrar Sesión
#         tb.Button(self.sidebar_frame, text="Cerrar Sesión", command=logout_callback,
#                   bootstyle="danger-outline", cursor="hand2").pack(fill="x", padx=10, pady=5,
#                                                                    side=BOTTOM)  # Se pega al fondo del sidebar
#
#         # --- Área de Contenido Principal ---
#         self.content_frame = tb.Frame(self, bootstyle="dark")
#         self.content_frame.grid(row=0, column=1, sticky="nsew")
#         self.content_frame.grid_columnconfigure(0, weight=1)
#         self.content_frame.grid_rowconfigure(0, weight=1)
#
#         self.current_content = None
#         self.show_user_management()  # Muestra la gestión de usuarios por defecto al iniciar
#
#     def show_user_management(self):
#         """
#         Muestra la vista de gestión de usuarios en el área de contenido principal.
#         """
#         if self.current_content:
#             self.current_content.destroy()  # Destruye la vista anterior si existe
#         self.current_content = UserManagementView(self.content_frame)
#         self.current_content.pack(expand=True, fill="both")
#
#
# # --- gui/user_management_view.py ---
# # Vista para la gestión de usuarios (tabla, botones de acción).
#
# class UserManagementView(tb.Frame):
#     def __init__(self, master):
#         super().__init__(master, padding=20)
#         self.master = master
#         self.grid_columnconfigure(0, weight=1)  # Columna principal para la tabla
#         self.grid_rowconfigure(1, weight=1)  # Fila para la tabla, para que se expanda
#
#         # Título de la sección
#         tb.Label(self, text="Gestión de Usuarios", font=("Inter", 20, "bold"), bootstyle="inverse-light").grid(row=0,
#                                                                                                                column=0,
#                                                                                                                pady=10,
#                                                                                                                sticky="w")
#
#         # Toolbar de acciones (Añadir, Editar, Eliminar)
#         toolbar_frame = tb.Frame(self, bootstyle="dark")
#         toolbar_frame.grid(row=0, column=1, pady=10, sticky="e")  # Alineado a la derecha
#         tb.Button(toolbar_frame, text="Añadir Usuario", command=self._add_user_dialog, bootstyle="success-outline",
#                   cursor="hand2").pack(side="left", padx=5)
#         tb.Button(toolbar_frame, text="Editar Usuario", command=self._edit_user_dialog, bootstyle="info-outline",
#                   cursor="hand2").pack(side="left", padx=5)
#         tb.Button(toolbar_frame, text="Eliminar Usuario", command=self._delete_user, bootstyle="danger-outline",
#                   cursor="hand2").pack(side="left", padx=5)
#
#         # Tabla de usuarios (Treeview)
#         columns = ("id", "username", "full_name", "email", "role", "status")
#         self.user_tree = tb.Treeview(self, columns=columns, show="headings", bootstyle="dark")
#         self.user_tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)  # Ocupa ambas columnas
#
#         # Scrollbar vertical para la tabla
#         scrollbar = tb.Scrollbar(self, orient="vertical", command=self.user_tree.yview, bootstyle="dark")
#         scrollbar.grid(row=1, column=2, sticky="ns")
#         self.user_tree.configure(yscrollcommand=scrollbar.set)
#
#         # Configuración de las cabeceras y ancho de las columnas de la tabla
#         for col in columns:
#             self.user_tree.heading(col, text=col.replace("_", " ").title(),
#                                    anchor="center")  # Nombres de columnas legibles
#             self.user_tree.column(col, width=100, anchor="center")
#
#         self.user_tree.column("id", width=50, stretch=False)  # ID no se estira
#         self.user_tree.column("username", width=150)
#         self.user_tree.column("full_name", width=200)
#         self.user_tree.column("email", width=200)
#         self.user_tree.column("role", width=120)
#         self.user_tree.column("status", width=80)
#
#         # Cargar usuarios al iniciar la vista
#         self.load_users()
#
#     def load_users(self):
#         """
#         Carga los usuarios desde la base de datos y los muestra en la tabla.
#         """
#         # Limpiar la tabla antes de cargar nuevos datos
#         for i in self.user_tree.get_children():
#             self.user_tree.delete(i)
#
#         users = get_all_users()
#         for user in users:
#             # Insertar cada usuario como una fila en la tabla
#             self.user_tree.insert("", "end", values=(
#             user['id'], user['username'], user['full_name'], user['email'], user['role'],
#             "Activo" if user['status'] == 1 else "Inactivo"))
#
#     def _add_user_dialog(self):
#         """
#         Abre el diálogo para añadir un nuevo usuario.
#         """
#         # Pasa el callback para recargar la tabla después de añadir
#         AddUserDialog(self.master, self.load_users)
#
#     def _edit_user_dialog(self):
#         """
#         Abre el diálogo para editar el usuario seleccionado.
#         """
#         selected_item = self.user_tree.selection()
#         if not selected_item:
#             messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario para editar.")
#             return
#
#         # Obtiene el ID del usuario seleccionado de la tabla
#         user_id = self.user_tree.item(selected_item, "values")[0]
#         # Pasa el ID del usuario y el callback para recargar la tabla
#         EditUserDialog(self.master, user_id, self.load_users)
#
#     def _delete_user(self):
#         """
#         Elimina el usuario seleccionado de la base de datos.
#         """
#         selected_item = self.user_tree.selection()
#         if not selected_item:
#             messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario para eliminar.")
#             return
#
#         # Obtiene el ID y el nombre de usuario del elemento seleccionado
#         user_id = self.user_tree.item(selected_item, "values")[0]
#         username = self.user_tree.item(selected_item, "values")[1]
#
#         # Pide confirmación antes de eliminar
#         if messagebox.askyesno("Confirmar Eliminación",
#                                f"¿Estás seguro de que quieres eliminar a '{username}'? Esta acción es irreversible."):
#             if delete_user(user_id):
#                 messagebox.showinfo("Éxito", f"Usuario '{username}' eliminado correctamente.")
#                 self.load_users()  # Recarga la tabla para reflejar el cambio
#             else:
#                 messagebox.showerror("Error", f"No se pudo eliminar al usuario '{username}'.")
#
#
# # --- gui/add_user_dialog.py ---
# # Diálogo modal para añadir un nuevo usuario.
#
# class AddUserDialog(tb.Toplevel):
#     def __init__(self, master, refresh_callback):
#         super().__init__(master, bootstyle="dark")
#         self.title("Añadir Nuevo Usuario")
#         self.geometry("450x500")  # Tamaño del diálogo
#         self.transient(master)  # Hace que la ventana sea modal y se cierre con la principal
#         self.grab_set()  # Bloquea la interacción con la ventana principal mientras está abierto
#         self.refresh_callback = refresh_callback  # Callback para recargar la tabla de usuarios
#
#         # Centrar la ventana Toplevel
#         self.update_idletasks()
#         x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
#         y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
#         self.geometry(f"+{x}+{y}")
#
#         main_frame = tb.Frame(self, padding=20)
#         main_frame.pack(expand=True, fill="both")
#
#         # Configuración de las columnas para las etiquetas y los campos de entrada
#         main_frame.grid_columnconfigure(0, weight=0)  # Columna de etiquetas
#         main_frame.grid_columnconfigure(1, weight=1)  # Columna de entradas (expandible)
#
#         # Campos del formulario
#         labels_text = ["Nombre de Usuario:", "Contraseña:", "Confirmar Contraseña:", "Nombre Completo:",
#                        "Correo Electrónico:", "Rol:", "Estado:"]
#         self.entries = {}  # Diccionario para almacenar las referencias a los widgets de entrada
#
#         for i, text in enumerate(labels_text):
#             tb.Label(main_frame, text=text, bootstyle="inverse-light", font=("Inter", 10)).grid(row=i, column=0,
#                                                                                                 sticky="w", pady=5)
#
#             if text == "Contraseña:" or text == "Confirmar Contraseña:":
#                 entry = tb.Entry(main_frame, show="*", bootstyle="dark")  # Campo de contraseña oculto
#             elif text == "Rol:":
#                 roles = ["Desarrollador", "Tester", "Diseñador", "Gerente", "Administrador"]
#                 entry = tb.Combobox(main_frame, values=roles, state="readonly", bootstyle="dark")  # Combobox para roles
#                 entry.set("Desarrollador")  # Valor por defecto
#             elif text == "Estado:":
#                 entry = tb.Checkbutton(main_frame, text="Activo",
#                                        bootstyle="success-round-toggle")  # Checkbutton para estado
#                 entry.state(['selected'])  # Marcado por defecto como Activo
#             else:
#                 entry = tb.Entry(main_frame, bootstyle="dark")  # Campos de texto normales
#
#             entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
#             self.entries[text] = entry  # Guardar referencia al widget
#
#         # Botón de Guardar Usuario
#         tb.Button(main_frame, text="Guardar Usuario", command=self._save_user, bootstyle="success",
#                   cursor="hand2").grid(row=len(labels_text), column=0, columnspan=2, pady=20)
#
#     def _save_user(self):
#         """
#         Recopila los datos del formulario y guarda el nuevo usuario en la base de datos.
#         """
#         username = self.entries["Nombre de Usuario:"].get().strip()
#         password = self.entries["Contraseña:"].get()
#         confirm_password = self.entries["Confirmar Contraseña:"].get()
#         full_name = self.entries["Nombre Completo:"].get().strip()
#         email = self.entries["Correo Electrónico:"].get().strip()
#         role = self.entries["Rol:"].get()
#         status = 1 if 'selected' in self.entries["Estado:"].state() else 0
#
#         # Validaciones básicas
#         if not all([username, password, confirm_password, full_name, email, role]):
#             messagebox.showwarning("Campos Requeridos", "Por favor, completa todos los campos.")
#             return
#
#         if password != confirm_password:
#             messagebox.showwarning("Contraseña", "Las contraseñas no coinciden.")
#             return
#
#         if len(password) < 6:
#             messagebox.showwarning("Contraseña", "La contraseña debe tener al menos 6 caracteres.")
#             return
#
#         hashed_password = hash_password(password)  # Hashear la contraseña
#
#         if add_user(username, hashed_password, full_name, email, role, status):
#             messagebox.showinfo("Éxito", "Usuario añadido correctamente.")
#             self.refresh_callback()  # Llama al callback para recargar la tabla
#             self.destroy()  # Cierra el diálogo
#         else:
#             messagebox.showerror("Error", "No se pudo añadir el usuario. El nombre de usuario podría ya existir.")
#
#
# # --- gui/edit_user_dialog.py ---
# # Diálogo modal para editar un usuario existente.
#
# class EditUserDialog(tb.Toplevel):
#     def __init__(self, master, user_id, refresh_callback):
#         super().__init__(master, bootstyle="dark")
#         self.title(f"Editar Usuario (ID: {user_id})")
#         self.geometry("450x500")
#         self.transient(master)
#         self.grab_set()
#         self.user_id = user_id
#         self.refresh_callback = refresh_callback
#
#         # Centrar la ventana Toplevel
#         self.update_idletasks()
#         x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
#         y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
#         self.geometry(f"+{x}+{y}")
#
#         main_frame = tb.Frame(self, padding=20)
#         main_frame.pack(expand=True, fill="both")
#
#         main_frame.grid_columnconfigure(0, weight=0)
#         main_frame.grid_columnconfigure(1, weight=1)
#
#         labels_text = ["Nombre de Usuario:", "Nombre Completo:", "Correo Electrónico:", "Rol:", "Estado:"]
#         self.entries = {}
#         for i, text in enumerate(labels_text):
#             tb.Label(main_frame, text=text, bootstyle="inverse-light", font=("Inter", 10)).grid(row=i, column=0,
#                                                                                                 sticky="w", pady=5)
#
#             if text == "Rol:":
#                 roles = ["Desarrollador", "Tester", "Diseñador", "Gerente", "Administrador"]
#                 entry = tb.Combobox(main_frame, values=roles, state="readonly", bootstyle="dark")
#             elif text == "Estado:":
#                 entry = tb.Checkbutton(main_frame, text="Activo", bootstyle="success-round-toggle")
#             else:
#                 entry = tb.Entry(main_frame, bootstyle="dark")
#
#             entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
#             self.entries[text] = entry
#
#         # Cargar los datos del usuario actual en el formulario
#         self._load_user_data()
#
#         tb.Button(main_frame, text="Guardar Cambios", command=self._save_changes, bootstyle="info",
#                   cursor="hand2").grid(row=len(labels_text), column=0, columnspan=2, pady=20)
#
#     def _load_user_data(self):
#         """
#         Carga los datos del usuario seleccionado en los campos del formulario.
#         """
#         user = get_user_by_id(self.user_id)
#         if user:
#             self.entries["Nombre de Usuario:"].insert(0, user['username'])
#             self.entries["Nombre Completo:"].insert(0, user['full_name'])
#             self.entries["Correo Electrónico:"].insert(0, user['email'])
#             self.entries["Rol:"].set(user['role'])
#             if user['status'] == 1:
#                 self.entries["Estado:"].state(['selected'])
#             else:
#                 self.entries["Estado:"].state(['!selected'])
#         else:
#             messagebox.showerror("Error", "No se pudo cargar la información del usuario.")
#             self.destroy()
#
#     def _save_changes(self):
#         """
#         Recopila los datos del formulario y actualiza el usuario en la base de datos.
#         """
#         username = self.entries["Nombre de Usuario:"].get().strip()
#         full_name = self.entries["Nombre Completo:"].get().strip()
#         email = self.entries["Correo Electrónico:"].get().strip()
#         role = self.entries["Rol:"].get()
#         status = 1 if 'selected' in self.entries["Estado:"].state() else 0
#
#         if not all([username, full_name, email, role]):
#             messagebox.showwarning("Campos Requeridos", "Por favor, completa todos los campos.")
#             return
#
#         if update_user(self.user_id, username, full_name, email, role, status):
#             messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
#             self.refresh_callback()  # Recarga la tabla
#             self.destroy()  # Cierra el diálogo
#         else:
#             messagebox.showerror("Error",
#                                  "No se pudo actualizar el usuario. El nombre de usuario podría ya existir para otro usuario.")
#
#
# # --- gui/app.py ---
# # Clase principal de la aplicación que gestiona las vistas.
#
# class App:
#     def __init__(self, master):
#         self.master = master
#         master.title("NexusForge - Gestión de Usuarios")
#         master.geometry("1200x700")  # Tamaño inicial de la ventana
#         master.minsize(800, 600)  # Tamaño mínimo de la ventana
#
#         self.current_user = None  # Almacena el objeto del usuario logueado
#
#         self.show_login_view()  # Muestra la vista de login al iniciar
#
#     def show_login_view(self):
#         """
#         Muestra la pantalla de inicio de sesión.
#         """
#         # Destruye cualquier widget existente en la ventana principal
#         for widget in self.master.winfo_children():
#             widget.destroy()
#         login_frame = LoginView(self.master, self.login_success)
#         login_frame.pack(expand=True, fill="both")
#
#     def login_success(self, user):
#         """
#         Callback que se ejecuta cuando el inicio de sesión es exitoso.
#         """
#         self.current_user = user
#         self.show_dashboard_view()  # Muestra el dashboard
#
#     def show_dashboard_view(self):
#         """
#         Muestra la pantalla del dashboard principal.
#         """
#         # Destruye cualquier widget existente
#         for widget in self.master.winfo_children():
#             widget.destroy()
#         dashboard_frame = DashboardView(self.master, self.current_user, self.logout)
#         dashboard_frame.pack(expand=True, fill="both")
#
#     def logout(self):
#         """
#         Cierra la sesión del usuario actual.
#         """
#         self.current_user = None
#         messagebox.showinfo("Sesión", "Has cerrado sesión.")
#         self.show_login_view()  # Vuelve a la pantalla de login
#
#
# # --- Ejecución principal ---
# if __name__ == "__main__":
#     # Asegúrate de que la base de datos y las tablas existan
#     create_db_and_tables()
#     # Añade un usuario administrador inicial si no hay ninguno
#     add_initial_admin()
#
#     # Inicializa la ventana principal de Tkinter con el tema oscuro de ttkbootstrap
#     root = tb.Window(themename="darkly")  # "darkly" es un tema oscuro de ttkbootstrap
#
#     # Crea una instancia de la aplicación
#     app = App(root)
#
#     # Inicia el bucle principal de eventos de Tkinter
#     root.mainloop()